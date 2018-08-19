from datetime import datetime, timedelta
import threading

from django.core.mail import send_mail
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import FormView, TemplateView, ListView

from restaurants.utils import get_coordinates, positions_distance, count_bookings
from user_management.models import Restaurant
from .forms import *


class SearchView(FormView):
    form_class = SearchForm
    # success_url = 'search/client_bookings.html'

    def form_valid(self, form):
        return super(SearchView, self).form_valid(form)


class IndexView(SearchView):
    template_name = 'booking/index.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(IndexView, self).get_context_data(**kwargs)
        context['welcome_message'] = 'Benvenuto nella homepage di Restaurants'
        return context


class ResultsView(SearchView):
    template_name = 'booking/results.html'

    def get_initial(self):
        if self.request.GET:
            initial = self.request.GET.dict()
            initial['services'] = self.request.GET.getlist('services')
            initial['kitchenTypes'] = self.request.GET.getlist('kitchenTypes')
            return initial
        else:
            return super(ResultsView, self).get_initial()

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ResultsView, self).get_context_data(**kwargs)
        restaurants_available = Restaurant.objects.all()
        restaurants_busy = []
        if 'services' in self.request.GET:
            services = self.request.GET.getlist('services')
            restaurants_available = restaurants_available.filter(services__in=services).annotate(
                num_services=Count('services')).filter(num_services=services.__len__())
        if 'kitchenTypes' in self.request.GET:
            kitchen_types = self.request.GET.getlist('kitchenTypes')
            restaurants_available = restaurants_available.filter(kitchen_types__in=kitchen_types).annotate(
                num_kitchen_types=Count('kitchen_types')).filter(num_kitchen_types=kitchen_types.__len__())

        search_position = get_coordinates(self.request.GET['site'])
        print(search_position)
        search_datetime = timezone.make_aware(datetime.strptime(
            self.request.GET['date'] + '-' + self.request.GET['time'], '%d/%m/%Y-%H:%M'),
            timezone.get_current_timezone())
        for restaurant in restaurants_available:
            if search_position:
                # params['address'] = restaurant.city + ', ' + restaurant.address
                lng = restaurant.longitude
                lat = restaurant.latitude
                if lng and lat:
                    restaurant_position = {
                        'lat': lat,
                        'lng': lng
                    }
                    print(restaurant_position)
                    distance = positions_distance(search_position, restaurant_position)
                    print(distance)
                    if distance > 50:
                        print('entro nella condizione')
                        restaurants_available = restaurants_available.exclude(id=restaurant.id)
                        break

            end_time = search_datetime + timedelta(minutes=restaurant.booking_duration)
            occupied_places = restaurant.restaurant_bookings.filter(
                (Q(start_time__lte=search_datetime) & Q(end_time__gte=search_datetime)) |
                (Q(start_time__lte=end_time) & Q(end_time__gte=end_time)))
            occupied_places = occupied_places.filter(state=Booking.STATES[1][0])
            occupied_places = occupied_places.aggregate(Sum('n_places'))['n_places__sum']
            if not occupied_places:
                occupied_places = 0
            if occupied_places + int(self.request.GET['n_clients']) > restaurant.n_places:
                restaurants_available = restaurants_available.exclude(id=restaurant.id)
                restaurants_busy.append(restaurant)

        context['restaurants_available'] = restaurants_available
        context['restaurants_busy'] = restaurants_busy
        context['datetime'] = datetime.strptime(self.request.GET['date']+'-'+self.request.GET['time'], '%d/%m/%Y-%H:%M')
        return context


class RestaurantDetailView(FormView):
    form_class = BookingForm
    template_name = 'booking/restaurant_detail.html'

    def get_success_url(self):
        return self.request.path

    def get_initial(self):
        initial = super(RestaurantDetailView, self).get_initial()
        if 'n_places' in self.request.GET:
            initial['n_places'] = self.request.GET['n_places']
        return initial

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        context['restaurant'] = restaurant
        return context

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        start = form.cleaned_data['start_time']
        end = start + timedelta(minutes=restaurant.booking_duration)
        Booking.objects.create(
            client=self.request.user,
            restaurant=restaurant,
            start_time=start,
            end_time=end,
            n_places=form.cleaned_data['n_places'],
            state=form.cleaned_data['state']
        )
        return super(RestaurantDetailView, self).form_valid(form)


class RestaurantBookingsView(TemplateView):
    template_name = 'booking/restaurant_bookings.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantBookingsView, self).get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        context['total_places'] = restaurant.n_places
        context['occupied_places'] = count_bookings(restaurant.id, datetime.now())
        return context


class ClientBookingsView(ListView):
    template_name = 'booking/client_bookings.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Booking.objects.filter(client=self.request.user)
        return queryset


def delete_booking(request):
    booking_id = request.POST['id']
    booking = Booking.objects.get(id=booking_id)
    restaurant_id = booking.restaurant.id
    start = booking.start_time
    end = booking.end_time
    booking.delete()
    check_bookings_to_confirm(start, end, restaurant_id)
    return JsonResponse({})


def edit_booking(request):
    booking_id = request.POST['id']
    booking = Booking.objects.get(id=booking_id)
    restaurant_id = booking.restaurant.id
    start = booking.start_time
    end = booking.end_time

    booking.n_places = request.POST['n_places']
    start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%d-%H-%M-%S'),
                                     timezone.get_current_timezone())
    booking.start_time = start_time
    booking.end_time = start_time + timedelta(minutes=booking.restaurant.booking_duration)
    booking.state = request.POST['state']
    booking.save()

    check_bookings_to_confirm(start, end, restaurant_id)
    return JsonResponse({})


def check_availability(request):
    response = {}
    n_places = request.POST['n_places']
    restaurant_id = request.POST['restaurant_id']
    start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%d-%H-%M-%S'),
                                     timezone.get_current_timezone())
    restaurant = Restaurant.objects.get(id=restaurant_id)
    end_time = start_time + timedelta(minutes=restaurant.booking_duration)
    occupied_places = restaurant.restaurant_bookings.filter(
        (Q(start_time__lte=start_time) & Q(end_time__gte=start_time)) |
        (Q(start_time__lte=end_time) & Q(end_time__gte=end_time)))
    occupied_places = occupied_places.filter(state=Booking.STATES[1][0])
    if 'booking_id' in request.POST:
        occupied_places = occupied_places.exclude(id=request.POST['booking_id'])
    occupied_places = occupied_places.aggregate(Sum('n_places'))['n_places__sum']
    if not occupied_places:
        occupied_places = 0
    if occupied_places + int(n_places) > restaurant.n_places:
        response['result'] = 'busy'
        response['state'] = Booking.STATES[0][0]
    else:
        response['result'] = 'ok'
        response['state'] = Booking.STATES[1][0]
    return JsonResponse(response)


def check_bookings_to_confirm(start, end, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    bookings = Booking.objects.filter(restaurant=restaurant).filter(
        (Q(start_time__lte=start) & Q(end_time__gte=start)) |
        (Q(start_time__lte=end) & Q(end_time__gte=end)))
    confirmed = bookings.filter(state=Booking.STATES[1][0])
    not_confirmed = bookings.filter(state=Booking.STATES[0][0])
    occupied_places = confirmed.aggregate(Sum('n_places'))['n_places__sum']
    if not occupied_places:
        occupied_places = 0
    added = 0
    for booking in not_confirmed:
        if occupied_places + added + booking.n_places <= restaurant.n_places:
            booking.state = Booking.STATES[1][0]
            booking.save()
            added = added + booking.n_places

            info_email = {
                'restaurant_name':  restaurant.name,
                'booking_start_time': booking.start_time,
                'client_email': booking.client.email
            }
            thr = threading.Thread(target=send_confirm_mail, kwargs=info_email)
            thr.start()


def send_confirm_mail(restaurant_name, booking_start_time, client_email):
    send_mail(
        'Prenotazione confermata',
        'La prenotazione presso il ristorante ' + restaurant_name +
        ' è stata confermata.\nLe ricordiamo che la prenotazione è valida per il giorno ' +
        booking_start_time.strftime('%d/%m/%Y') + ' alle ' +
        booking_start_time.strftime('%H:%M') + '.',
        'restaurant.noreply@gmail.com',
        [client_email],
        fail_silently=False,
    )
