from django.views.generic.edit import FormView
from .forms import *
from .models import Restaurant


class SearchView(FormView):
    form_class = SearchForm
    # success_url = 'search/results.html'

    def form_valid(self, form):
        return super().form_valid(form)


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
            return initial
        else:
            return super(ResultsView, self).get_initial()

    def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.all()
        return context