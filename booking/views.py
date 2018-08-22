from datetime import datetime, timedelta
from operator import itemgetter

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Q
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, ListView, CreateView

from booking.utils import check_bookings_to_confirm
from restaurants.utils import get_coordinates, count_bookings
from user_management.models import Restaurant, User
from .forms import *


class SearchView(FormView):
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['search_button'] = 'Cerca'
        return context


class IndexView(SearchView):
    template_name = 'booking/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['webpage_title'] = 'Home'
        context['title'] = 'Benvenuto nella homepage di Restaurants'
        return context


class ResultsView(SearchView):
    template_name = 'booking/results.html'

    def get_initial(self):
        if self.request.GET:
            initial = self.request.GET.dict()
            initial['services'] = self.request.GET.getlist('services')
            initial['kitchen_types'] = self.request.GET.getlist('kitchen_types')
            return initial
        else:
            return super(ResultsView, self).get_initial()

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)

        context['restaurants_available_title'] = 'Ristoranti disponibili'
        context['restaurants_busy_title'] = 'Ristoranti pieni'
        context['address_label'] = 'Indirizzo:'
        context['kitchen_types_label'] = 'Tipi di cucina:'
        context['services_label'] = 'Servizi:'
        context['button_text'] = 'Dettagli'
        context['webpage_title'] = 'Risultati'

        try:
            restaurants = Restaurant.objects.all()
            restaurants_busy = []
            restaurants_available = []
            if 'services' in self.request.GET:
                services = self.request.GET.getlist('services')
                restaurants = restaurants.filter(services__in=services).annotate(
                    num_services=Count('services')).filter(num_services=services.__len__())
            if 'kitchen_types' in self.request.GET:
                kitchen_types = self.request.GET.getlist('kitchen_types')
                restaurants = restaurants.filter(kitchen_types__in=kitchen_types).annotate(
                    num_kitchen_types=Count('kitchen_types')).filter(num_kitchen_types=kitchen_types.__len__())
            restaurants = restaurants.filter(n_places__gte=self.request.GET['n_clients'])

            search_position = get_coordinates(self.request.GET['site'])
            for restaurant in restaurants:
                distance = None
                if search_position:
                    distance = restaurant.get_distance_from_position(search_position)
                    if distance and distance > 50:
                        continue
                if not distance:
                    distance = 51

                search_datetime = timezone.make_aware(datetime.strptime(
                    self.request.GET['date'] + '-' + self.request.GET['time'], '%d/%m/%Y-%H:%M'),
                    timezone.get_current_timezone())
                end_time = search_datetime + timedelta(minutes=restaurant.booking_duration)
                occupied_places = restaurant.bookings.filter(
                    (Q(start_time__lte=search_datetime) & Q(end_time__gte=search_datetime)) |
                    (Q(start_time__lte=end_time) & Q(end_time__gte=end_time)))
                occupied_places = occupied_places.filter(state=Booking.STATES[1][0])
                occupied_places = occupied_places.aggregate(Sum('n_places'))['n_places__sum']
                if not occupied_places:
                    occupied_places = 0
                element = {
                    'restaurant': restaurant,
                    'distance': distance
                }
                if occupied_places + int(self.request.GET['n_clients']) > restaurant.n_places:
                    restaurants_busy.append(element)
                else:
                    restaurants_available.append(element)

            context['restaurants_available'] = sorted(restaurants_available, key=itemgetter('distance'))
            context['restaurants_busy'] = restaurants_busy
            context['datetime'] = datetime.strptime(self.request.GET['date']+'-'+self.request.GET['time'],
                                                    '%d/%m/%Y-%H:%M')
        except KeyError:
            context['error_message'] = 'Problema nel passaggio dei parametri'
        return context


class RestaurantDetailView(CreateView):
    form_class = BookingForm
    model = Booking
    template_name = 'booking/restaurant_detail.html'

    def get_success_url(self):
        return self.request.path

    def get_initial(self):
        initial = super(RestaurantDetailView, self).get_initial()
        if 'n_places' in self.request.GET:
            initial['n_places'] = self.request.GET['n_places']
        else:
            initial['n_places'] = 1
        return initial

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        context['restaurant'] = restaurant

        context['address_label'] = 'Indirizzo:'
        context['kitchen_types_label'] = 'Tipi di cucina:'
        context['services_label'] = 'Servizi:'
        context['booking_label'] = 'Prenota:'
        context['menu_label'] = 'Menù:'
        context['n_places_label'] = 'Nº posti:'
        context['availability_button'] = 'Disponibilità'
        context['book_button'] = 'Prenota'
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated and self.request.user.is_client():
            restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
            booking = form.save(commit=False)
            booking.client = self.request.user
            booking.restaurant = restaurant
            booking.end_time = booking.calculate_end_time()
            booking.save()
            messages.success(self.request, 'Prenotazione effettuata con successo.')
            return super(RestaurantDetailView, self).form_valid(form)
        else:
            params = '?'
            for key in self.request.GET.keys():
                params = params + '%26' + key + '=' + self.request.GET[key]
                params = params.replace('?%26', '?')
            return HttpResponseRedirect(reverse('user_management:registration') + "?next=" + self.request.path + params)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(User.is_restaurant), name='dispatch')
class RestaurantBookingsView(TemplateView):
    template_name = 'booking/restaurant_bookings.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantBookingsView, self).get_context_data(**kwargs)
        context['webpage_title'] = 'Prenotazioni'
        context['n_places_label'] = 'Posti prenotati:'

        try:
            restaurant = self.request.user.restaurant_information
            context['total_places'] = restaurant.n_places
            time = timezone.make_aware(datetime.now(), timezone.get_current_timezone()).replace(microsecond=0)
            context['occupied_places'] = count_bookings(restaurant.id, time)
        except Restaurant.DoesNotExist:
            context['error_message'] = 'Il ristorante relativo all\'utente non esiste più'
        return context

    def dispatch(self, *args, **kwargs):
        return super(RestaurantBookingsView, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(User.is_client), name='dispatch')
class ClientBookingsView(ListView):
    template_name = 'booking/client_bookings.html'
    now = timezone.make_aware(datetime.now(), timezone.get_current_timezone()).replace(microsecond=0)

    def get_queryset(self):
        queryset = Booking.objects.filter(client=self.request.user, start_time__gte=self.now)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientBookingsView, self).get_context_data(**kwargs)
        context['old_bookings'] = Booking.objects.filter(client=self.request.user, start_time__lt=self.now)

        context['webpage_title'] = 'Prenotazioni'
        context['active_bookings_title'] = 'Prenotazioni attive'
        context['old_bookings_title'] = 'Prenotazioni passate'
        context['address_label'] = 'Indirizzo:'
        context['name_label'] = 'Nome:'
        context['state_label'] = 'Stato:'
        context['date_label'] = 'Data:'
        context['n_places_label'] = 'Nº posti:'
        context['details_button'] = 'Dettagli'
        context['availability_button'] = 'Disponibilità'
        context['edit_button'] = 'Modifica'
        context['delete_button'] = 'Elimina'
        context['save_button'] = 'Salva'
        return context

    def dispatch(self, *args, **kwargs):
        return super(ClientBookingsView, self).dispatch(*args, **kwargs)


@login_required
@user_passes_test(User.is_client)
def delete_booking(request):
    if request.is_ajax():
        response = {}
        try:
            booking_id = request.POST['id']
            booking = Booking.objects.get(id=booking_id)
            restaurant_id = booking.restaurant.id
            start = booking.start_time
            end = booking.calculate_end_time()
            booking.delete()
            check_bookings_to_confirm(start, end, restaurant_id)
            response['result'] = 'success'
        except (Booking.DoesNotExist, KeyError):
            response['result'] = 'error'
        return JsonResponse(response)
    else:
        raise Http404


@login_required
@user_passes_test(User.is_client)
def edit_booking(request):
    if request.is_ajax():
        response = {}
        try:
            booking = Booking.objects.get(id=request.POST['id'])
            restaurant_id = booking.restaurant.id
            start = booking.start_time
            end = booking.calculate_end_time()

            booking.n_places = request.POST['n_places']
            start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%d-%H-%M-%S'),
                                             timezone.get_current_timezone())
            booking.start_time = start_time
            booking.end_time = booking.calculate_end_time()
            booking.state = request.POST['state']
            booking.save()

            check_bookings_to_confirm(start, end, restaurant_id)
            response['result'] = 'success'
        except (Booking.DoesNotExist, KeyError):
            response['result'] = 'error'
        return JsonResponse(response)
    else:
        raise Http404


def check_availability(request):
    if request.is_ajax():
        response = {}
        try:
            response['result'] = 'success'
            start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%d-%H-%M-%S'),
                                             timezone.get_current_timezone())
            restaurant = Restaurant.objects.get(id=request.POST['restaurant_id'])
            end_time = start_time + timedelta(minutes=restaurant.booking_duration)
            occupied_places = restaurant.bookings.filter(
                (Q(start_time__lte=start_time) & Q(end_time__gte=start_time)) |
                (Q(start_time__lte=end_time) & Q(end_time__gte=end_time)))
            if 'booking_id' in request.POST:
                occupied_places = occupied_places.exclude(id=request.POST['booking_id'])
            if 'client_id' in request.POST:
                client = User.objects.get(id=request.POST['client_id'])
                client = occupied_places.filter(client=client)
                if not len(client) == 0:
                    response['state'] = -1
                    return JsonResponse(response)

            occupied_places = occupied_places.filter(state=Booking.STATES[1][0])
            occupied_places = occupied_places.aggregate(Sum('n_places'))['n_places__sum']
            if not occupied_places:
                occupied_places = 0
            if occupied_places + int(request.POST['n_places']) > restaurant.n_places:
                response['state'] = Booking.STATES[0][0]
            else:
                response['state'] = Booking.STATES[1][0]
        except (Restaurant.DoesNotExist, KeyError):
            response['result'] = 'error'
        return JsonResponse(response)
    else:
        raise Http404
