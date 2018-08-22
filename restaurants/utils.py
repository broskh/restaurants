from math import radians, sin, atan2, sqrt, cos
import requests
from django.db.models import Sum, Q

from booking.models import Booking
from user_management.models import Restaurant

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'


def get_coordinates(address):
    params = {
        'address': address,
        # 'sensor': 'false',
        'region': 'it',
        'key': 'AIzaSyCtDBXSlOMuLNiKQyWjgJyJw9K8ZC5SndA',
    }
    response = requests.get(GOOGLE_MAPS_API_URL, params=params).json()
    if 'error_message' not in response:
        return response['results'][0]['geometry']['location']
    else:
        return None


def count_bookings(restaurant_id, time):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        bookings = Booking.objects.filter(restaurant=restaurant).filter(Q(start_time__lte=time) & Q(end_time__gte=time))
        bookings = bookings.filter(state=Booking.STATES[1][0])
        occupied_places = bookings.aggregate(Sum('n_places'))['n_places__sum']
        if not occupied_places:
            occupied_places = 0
        return occupied_places
    except (Restaurant.DoesNotExist):
        raise Restaurant.DoesNotExist