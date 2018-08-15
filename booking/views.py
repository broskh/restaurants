from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
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
            restaurant = restaurant,
            start_time = start,
            end_time = end,
            n_places = form.cleaned_data['n_places'],
            state = 1
        )
        return super(RestaurantDetailView, self).form_valid(form)


def delete_booking(request):
    id = request.POST['id']
    Booking.objects.get(id=id).delete()
    return JsonResponse({})


def edit_booking(request):
    id = request.POST['id']
    booking = Booking.objects.get(id=id)
    booking.n_places = request.POST['n_places']
    start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%d-%H-%M-%S'), timezone.get_current_timezone())
    booking.start_time = start_time
    booking.end_time = start_time + timedelta(minutes=booking.restaurant.booking_duration)
    booking.save()
    return JsonResponse({})
