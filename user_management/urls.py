from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user-info/(?P<user_id>[0-9]+)/$', views.ClientInfoView.as_view(), name='user_info'),
    url(r'^restaurant-info/(?P<restaurant_id>[0-9]+)/$', views.RestaurantInfoView.as_view(), name='restaurant_info'),
]