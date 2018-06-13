from django.contrib import admin
from .models import User, Service, KitchenType, Restaurant, RestaurantImage, MenuCategory, MenuVoice


admin.site.register(User)
admin.site.register(Service)
admin.site.register(KitchenType)
admin.site.register(Restaurant)
admin.site.register(RestaurantImage)
admin.site.register(MenuCategory)
admin.site.register(MenuVoice)