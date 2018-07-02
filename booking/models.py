from django.db import models
from user_management.models import User


class Booking(models.Model):
    STATES = (
        (1, 'In attesa'),
        (2, 'Confermata'),
    )

    client = models.ForeignKey(User, related_name='client')
    restaurant = models.ForeignKey(User, related_name='restaurant')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    n_places = models.PositiveIntegerField(default=1)
    state = models.PositiveSmallIntegerField(choices=STATES)
