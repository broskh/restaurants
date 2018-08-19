from datetime import datetime, timedelta

from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.views.generic.edit import FormView

from booking.models import Booking
from restaurants.utils import get_coordinates, positions_distance
from .forms import *
from .models import Restaurant


class SearchView(FormView):
    form_class = SearchForm
    # success_url = 'search/client_bookings.html'

    def form_valid(self, form):
        return super(SearchView, self).form_valid(form)


class IndexView(SearchView):
    template_name = 'search/index.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(IndexView, self).get_context_data(**kwargs)
        context['welcome_message'] = 'Benvenuto nella homepage di Restaurants'
        return context


class ResultsView(SearchView):
    template_name = 'search/results.html'

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
            restaurants_available = restaurants_available.filter(services__in=services).annotate(num_services=Count('services')).filter(num_services=services.__len__())
        if 'kitchenTypes' in self.request.GET:
            kitchen_types = self.request.GET.getlist('kitchenTypes')
            restaurants_available = restaurants_available.filter(kitchen_types__in=kitchen_types).annotate(num_kitchen_types=Count('kitchen_types')).filter(num_kitchen_types=kitchen_types.__len__())

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
                        'lat':lat,
                        'lng': lng
                    }
                    print(restaurant_position)
                    distance = positions_distance(search_position, restaurant_position)
                    print(distance)
                    if distance > 50:  #DA TESTARE
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