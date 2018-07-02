from django.views.generic.edit import FormView
from .forms import *


class ClientInfoView(FormView):
    form_class = UserInfoForm
    template_name = 'user_management/user-info.html'

    def form_valid(self, form):
        return super().form_valid(form)


class RestaurantInfoView(FormView):
    form_class = RestaurantInfoForm
    template_name = 'user_management/restaurant-info.html'

    def form_valid(self, form):
        return super().form_valid(form)
