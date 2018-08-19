from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user-info/(?P<user_id>[0-9]+)/$', views.UserInfoView.as_view(), name='user_info'),
    url(r'^restaurant-info/(?P<restaurant_id>[0-9]+)/$', views.RestaurantInfoView.as_view(), name='restaurant_info'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^count-restaurant-bookings/$', views.count_restaurant_bookings, name='count_restaurant_bookings'),
]
