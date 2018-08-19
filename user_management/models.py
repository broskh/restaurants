import os
from time import strftime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class KitchenType(models.Model):
    value = models.CharField(max_length=150)


class Service(models.Model):
    value = models.CharField(max_length=200)


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    kitchen_types = models.ManyToManyField(KitchenType, blank=True, name='kitchen_types')
    services = models.ManyToManyField(Service, blank=True)
    city = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    n_places = models.PositiveIntegerField()
    booking_duration = models.PositiveIntegerField()
    longitude = models.FloatField(default=None, blank=True, null=True)
    latitude = models.FloatField(default=None, blank=True, null=True)


class MenuCategory(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, related_name='menu_categories')


class MenuVoice(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    menu_category = models.ForeignKey(MenuCategory, related_name='menu_voices')


class RestaurantImage(models.Model):
    image = models.ImageField(upload_to=strftime('%Y/%m/%d/%H/%M/%S/'))
    restaurant = models.ForeignKey(Restaurant, related_name='images')

    def filename(self):
        return os.path.basename(self.image.name)


class User(AbstractUser):
    TYPES = (
        (1, 'admin'),
        (2, 'client'),
        (3, 'restaurant'),
    )

    user_type = models.PositiveSmallIntegerField(choices=TYPES, default=1)
    restaurant_information = models.OneToOneField(Restaurant, blank=True, null=True)
