from datetime import datetime, timedelta
import threading

from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import FormView

from search.models import Restaurant
from .forms import *


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
