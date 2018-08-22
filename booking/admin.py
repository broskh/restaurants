from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    fields = ['client', 'restaurant', 'n_places', 'start_time', 'end_time', 'state']
    list_display = ('id', 'client', 'restaurant', 'n_places', 'start_time', 'end_time', 'state')
    list_filter = ['client', 'restaurant', 'start_time', 'state']


admin.site.register(Booking, BookingAdmin)
