from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

from booking.models import Booking
from .forms import *


class ClientInfoView(FormView):
    form_class = UserInfoForm
    template_name = 'user_management/user_info.html'

    def form_valid(self, form):
        return super().form_valid(form)


class RestaurantInfoView(FormView):
    form_class = RestaurantInfoForm
    template_name = 'user_management/restaurant_info.html'

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RestaurantInfoView, self).get_context_data(**kwargs)
        context['loaded_images'] = User.objects.all()
        return context

    def form_valid(self, form):
        return super().form_valid(form)


class RestaurantBookingsView(TemplateView):
    template_name = 'user_management/restaurant_bookings.html'


class ClientBookingsView(ListView):
    template_name = 'user_management/client_bookings.html'

    model = Booking
    paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'user_management/registration.html'

    def form_valid(self, form):
        return super().form_valid(form)
