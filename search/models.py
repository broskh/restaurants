import os
from time import strftime

from django.db import models
from django.core.validators import MinValueValidator


class KitchenType(models.Model):
    value = models.CharField(max_length=150)


class Service(models.Model):
    value = models.CharField(max_length=200)


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    kitchen_types = models.ManyToManyField(KitchenType)
    services = models.ManyToManyField(Service)
    city = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    n_places = models.PositiveIntegerField()
    booking_duration = models.PositiveIntegerField()


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
