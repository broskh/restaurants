from django.http import request
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from .forms import *
from search.models import Restaurant


class RestaurantDetailView(DetailView):
    form = BookingForm
    model = Restaurant
    template_name = 'booking/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(DetailView, self).get_context_data(**kwargs)
        return context
