from math import radians, sin, atan2, sqrt, cos
import requests
from django.db.models import Sum, Q

from booking.models import Booking
from user_management.models import Restaurant

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
R = 6373.0


def positions_distance(position1, position2):

    lat1 = radians(position1['lat'])
    lon1 = radians(position1['lng'])
    lat2 = radians(position2['lat'])
    lon2 = radians(position2['lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_coordinates(address):
    params = {
        'address': address,
        # 'sensor': 'false',
        'region': 'it',
        'key': 'AIzaSyBbT3t_tmi01bh-GnHlmomML3KlkVYeNao',
    }
    response = requests.get(GOOGLE_MAPS_API_URL, params=params).json()
    print(response)
    if 'error_message' not in response:
        return response['results'][0]['geometry']['location']
    else:
        return None


def count_bookings(restaurant_id, time):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    bookings = Booking.objects.filter(restaurant=restaurant).filter(Q(start_time__lte=time) & Q(end_time__gte=time))
    bookings = bookings.filter(state=Booking.STATES[1][0])
    occupied_places = bookings.aggregate(Sum('n_places'))['n_places__sum']
    if not occupied_places:
        occupied_places = 0
    return occupied_places
