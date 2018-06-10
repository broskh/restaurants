from django.db import models
from enum import Enum
from user_managment import models as user_managment_models


class Booking(models.Model):
    STATES = (
        (1, 'In attesa'),
        (2, 'Confermata'),
    )

    client = models.ForeignKey(user_managment_models.User, related_name='client')
    restaurant = models.ForeignKey(user_managment_models.User, related_name='restaurant')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    nPlaces = models.PositiveIntegerField(default=1)
    state = models.PositiveSmallIntegerField(choices=STATES)