from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search-results$', views.ResultsView.as_view(), name='search_results'),
    url(r'^restaurant-detail/(?P<restaurant_id>[0-9]+)/$', views.RestaurantDetailView.as_view(),
        name='restaurant_detail'),
    url(r'^restaurant-bookings/(?P<restaurant_id>[0-9]+)/$', views.RestaurantBookingsView.as_view(),
        name='restaurant_bookings'),
    url(r'^client-bookings/(?P<user_id>[0-9]+)/$', views.ClientBookingsView.as_view(), name='client_bookings'),
    url(r'^delete-booking/$', views.delete_booking, name='delete_booking'),
    url(r'^edit-booking/$', views.edit_booking, name='edit_booking'),
    url(r'^check-availability/$', views.check_availability, name='check_availability'),
]
