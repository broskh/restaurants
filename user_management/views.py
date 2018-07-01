from django.views.generic.edit import FormView
from .forms import *


class ClientInfoView(FormView):
    form_class = ClientInfoForm
    template_name = 'user_management/client-info.html'
    # success_url = 'search/results.html'

    def form_valid(self, form):
        return super().form_valid(form)
