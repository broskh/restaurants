from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^detail/(?P<pk>[0-9]+)/$', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
]