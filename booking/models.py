from django.db import models

from user_management.models import User, Restaurant


class Booking(models.Model):
    STATES = (
        (0, 'In attesa'),
        (1, 'Confermata'),
    )

    client = models.ForeignKey(User, related_name='client_bookings')
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    n_places = models.PositiveIntegerField(default=1)
    state = models.PositiveSmallIntegerField(choices=STATES)
