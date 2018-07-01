from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^client-info/(?P<client_id>[0-9]+)/$', views.ClientInfoView.as_view(), name='client_info'),
]