from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from user_management.forms import UserChangeFormAdmin
from .models import User, Service, KitchenType, Restaurant, RestaurantImage, MenuCategory, MenuVoice


class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeFormAdmin

    fieldsets = [
        (None, {'fields': ['username', 'password', 'first_name', 'last_name', 'email', 'user_type',
                           'restaurant_information']}),
        ('Advanced', {'fields': ['is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'date_joined',
                                 'last_login'],
                      'classes': ['collapse']}),
    ]
    add_fieldsets = (
        (None, {'fields': ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'user_type',
                           'restaurant_information']}),
        ('Advanced', {'fields': ['is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'date_joined',
                                 'last_login'],
                      'classes': ['collapse']}),
    )
    list_display = ('username', 'user_type', 'first_name', 'last_name', 'email', 'restaurant_information')
    list_filter = ['user_type']
    search_fields = ['username', 'first_name', 'last_name', 'email']


class MenuCategoryInline(admin.StackedInline):
    model = MenuCategory
    extra = 1
    classes = ['collapse']


class MenuVoiceInline(admin.StackedInline):
    model = MenuVoice
    extra = 1


class RestaurantImageInline(admin.StackedInline):
    model = RestaurantImage
    extra = 1
    classes = ['collapse']


class RestaurantsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'city', 'address', 'n_places', 'booking_duration', 'kitchen_types', 'services',
                           'latitude', 'longitude']}),
    ]
    list_display = ('name', 'city', 'address', 'n_places', 'booking_duration', 'longitude', 'latitude')
    list_filter = ['kitchen_types', 'services']
    search_fields = ['name', 'city', 'address']
    inlines = [RestaurantImageInline, MenuCategoryInline]


class RestaurantImageAdmin(admin.ModelAdmin):
    fields = ['image', 'restaurant']
    list_display = ('image', 'restaurant')
    list_filter = ['restaurant']
    search_fields = ['image']


class MenuVoiceAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'menu_category']
    list_display = ('name', 'price', 'menu_category')
    list_filter = ['menu_category']
    search_fields = ['name']


class MenuCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'restaurant']
    list_display = ('name', 'restaurant')
    list_filter = ['restaurant']
    search_fields = ['name']
    inlines = [MenuVoiceInline]


admin.site.register(User, UserAdmin)
admin.site.register(Service)
admin.site.register(KitchenType)
admin.site.register(Restaurant, RestaurantsAdmin)
admin.site.register(RestaurantImage, RestaurantImageAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuVoice, MenuVoiceAdmin)
