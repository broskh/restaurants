from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user-info/(?P<user_id>[0-9]+)/$', views.UserInfoView.as_view(), name='user_info'),
    url(r'^restaurant-info/(?P<restaurant_id>[0-9]+)/$', views.RestaurantInfoView.as_view(), name='restaurant_info'),
    url(r'^restaurant-bookings/(?P<restaurant_id>[0-9]+)/$', views.RestaurantBookingsView.as_view(),
        name='restaurant_bookings'),
    url(r'^client-bookings/(?P<user_id>[0-9]+)/$', views.ClientBookingsView.as_view(), name='client_bookings'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^count-restaurant-bookings/$', views.count_restaurant_bookings, name='count_restaurant_bookings'),
]
