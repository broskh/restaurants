from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^detail/(?P<restaurant_id>[0-9]+)/$', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    url(r'^delete-booking/$', views.delete_booking, name='delete_booking'),
    url(r'^edit-booking/$', views.edit_booking, name='edit_booking'),
    url(r'^check-availability/$', views.check_availability, name='check_availability'),
]
