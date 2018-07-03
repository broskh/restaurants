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
    n_places = models.PositiveIntegerField(default=1)
    booking_duration = models.PositiveIntegerField(default=120)


class MenuCategory(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant)


class MenuVoice(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    menu_category = models.ForeignKey(MenuCategory)


class RestaurantImage(models.Model):
    position = models.PositiveIntegerField(default=1)
    image = models.ImageField()
    restaurant = models.ForeignKey(Restaurant)