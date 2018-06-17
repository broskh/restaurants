from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from user_managment.models import Service, KitchenType


# def index(request):
#     return render(request, 'booking/index.html')
from user_managment.models import Restaurant


class IndexView(TemplateView):
    template_name = 'booking/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all()
        kitchen_types = KitchenType.objects.all()
        context['services'] = services
        context['kitchen_types'] = kitchen_types
        return context


def search(request):
    try:
        site = request.POST['site']

        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError):
        return render(request, 'polls/detail.html', {'question': p, 'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',))


class ResultView(TemplateView):
    template_name = 'booking/result.html'
