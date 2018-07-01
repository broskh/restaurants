from django.contrib.auth.models import AbstractUser
from django.db import models
from search.models import Restaurant


class User(AbstractUser):
    TYPES = (
        (1, 'admin'),
        (2, 'client'),
        (3, 'restaurant'),
    )

    user_type = models.PositiveSmallIntegerField(choices=TYPES, default=1)
    restaurant_information = models.OneToOneField(Restaurant, blank=True, null=True)
