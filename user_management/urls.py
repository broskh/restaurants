from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user-info/$', views.UserInfoView.as_view(), name='user_info'),
    url(r'^restaurant-info/$', views.RestaurantInfoView.as_view(), name='restaurant_info'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^count-restaurant-bookings/$', views.count_restaurant_bookings, name='count_restaurant_bookings'),
]
