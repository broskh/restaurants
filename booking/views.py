from django.views.generic.base import TemplateView


# def index(request):
#     return render(request, 'booking/index.html')
from user_managment.models import Restaurant


class IndexView(TemplateView):
    template_name = 'booking/index.html'