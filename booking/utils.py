import threading

from django.core.mail import send_mail
from django.db.models import Sum, Q

from booking.models import Booking
from user_management.models import Restaurant


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
