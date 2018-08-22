import os
from math import radians, sin, atan2, sqrt, cos
from time import strftime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator


class KitchenType(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Service(models.Model):
    value = models.CharField(max_length=150)

    def __str__(self):
        return self.value


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    kitchen_types = models.ManyToManyField(KitchenType, blank=True, name='kitchen_types')
    services = models.ManyToManyField(Service, blank=True)
    city = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    n_places = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    booking_duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    longitude = models.FloatField(default=None, blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True)

    R = 6373.0

    def get_distance_from_position(self, position):
        if self.latitude and self.longitude:
            lat1 = radians(self.latitude)
            lon1 = radians(self.longitude)
            lat2 = radians(position['lat'])
            lon2 = radians(position['lng'])

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            return self.R * c
        return None

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, related_name='menu_categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MenuVoice(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    menu_category = models.ForeignKey(MenuCategory, related_name='menu_voices', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    image = models.ImageField(upload_to=strftime('%Y/%m/%d/%H/%M/%S/'))
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE)

    def filename(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return self.filename()


class User(AbstractUser):
    TYPES = (
        (1, 'Cliente'),
        (2, 'Ristorante'),
    )

    user_type = models.PositiveSmallIntegerField(choices=TYPES, blank=True, null=True)
    restaurant_information = models.OneToOneField(Restaurant, blank=True, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def is_client(self):
        if self.user_type == User.TYPES[0][0]:
            return True
        return False

    def is_restaurant(self):
        if self.user_type == User.TYPES[1][0]:
            return True
        return False

    def clean(self):
        super(User, self).clean()

        if self.user_type == self.TYPES[0][0] and self.restaurant_information:
            raise ValidationError('Client can not have a restaurant.')

    def __str__(self):
        return self.username
