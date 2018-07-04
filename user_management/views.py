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

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(RestaurantInfoView, self).get_context_data(**kwargs)
        context['loaded_images'] = User.objects.all()
        return context

    def form_valid(self, form):
        return super().form_valid(form)
