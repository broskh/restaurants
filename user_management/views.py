import json
import os
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect, Http404

from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView, CreateView

from restaurants.utils import get_coordinates, count_bookings
from .models import RestaurantImage, MenuCategory, MenuVoice
from .forms import *


@method_decorator(login_required, name='dispatch')
class UserInfoView(UpdateView):
    form_class = UserInfoForm
    model = User
    template_name = 'user_management/user_info.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfoView, self).get_context_data(**kwargs)
        context['title'] = 'Informazioni utente'
        context['webpage_title'] = 'Informazioni utente'
        context['save_button'] = 'Salva'
        return context

    def get_object(self, queryset=None):
        try:
            user = self.request.user
            if user:
                return user
            else:
                raise Http404
        except User.DoesNotExist:
            raise Http404

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        messages.success(self.request, 'Modifiche effettuate con successo.')
        return super(UserInfoView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(UserInfoView, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(User.is_restaurant), name='dispatch')
class RestaurantInfoView(UpdateView):
    form_class = RestaurantInfoForm
    model = Restaurant
    template_name = 'user_management/restaurant_info.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        try:
            restaurant = self.request.user.restaurant_information
            if restaurant:
                return restaurant
            else:
                raise Http404
        except Restaurant.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(RestaurantInfoView, self).get_context_data(**kwargs)
        context['title'] = 'Informazioni ristorante'
        context['webpage_title'] = 'Informazioni ristorante'
        context['save_button'] = 'Salva'
        return context

    def form_valid(self, form):
        restaurant = form.save(commit=False)
        if restaurant.address != form.cleaned_data['address'] or restaurant.city != form.cleaned_data['city']:
            position = get_coordinates(form.cleaned_data['city'] + ', ' + form.cleaned_data['address'])
            if position:
                restaurant.longitude = position['lng']
                restaurant.latitude = position['lat']
            else:
                restaurant.longitude = None
                restaurant.latitude = None

        files = self.request.FILES.getlist('load_image')
        for f in files:
            RestaurantImage.objects.create(
                image=f,
                restaurant=restaurant
            )

        if form.cleaned_data['remove_images']:
            for image_id in form.cleaned_data['remove_images'].split(','):
                try:
                    image = RestaurantImage.objects.get(id=image_id)
                    os.remove(image.image.path)
                    image.delete()
                except RestaurantImage.DoesNotExist:
                    pass

        add_voices = None
        if form.cleaned_data['add_voices']:
            add_voices = json.loads(form.cleaned_data['add_voices'])
        if form.cleaned_data['add_categories']:
            for category in json.loads(form.cleaned_data['add_categories']):
                new_category = MenuCategory.objects.create(
                    name=category['name'],
                    restaurant=restaurant
                )
                if add_voices:
                    for voice in add_voices:
                        if voice['category_id'] == category['id']:
                            voice['category_id'] = new_category.id

        if form.cleaned_data['remove_categories']:
            for category in form.cleaned_data['remove_categories'].split(','):
                try:
                    MenuCategory.objects.get(id=category).delete()
                except MenuCategory.DoesNotExist:
                    pass

        if add_voices:
            for voice in add_voices:
                category = MenuCategory.objects.get(id=voice['category_id'])
                MenuVoice.objects.create(
                    name=voice['name'],
                    price=voice['price'],
                    menu_category=category
                )

        if form.cleaned_data['remove_voices']:
            for voice in form.cleaned_data['remove_voices'].split(','):
                try:
                    MenuVoice.objects.get(id=voice).delete()
                except MenuVoice.DoesNotExist:
                    pass

        restaurant.save()
        messages.success(self.request, 'Modifiche effettuate con successo.')
        return super(RestaurantInfoView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super(RestaurantInfoView, self).dispatch(*args, **kwargs)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'user_management/registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'Registrazione'
        context['webpage_title'] = 'Registrazione'
        context['register_button'] = 'Registra'
        return context

    def get_success_url(self, **kwargs):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse('booking:index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        if int(user.user_type) == User.TYPES[1][0]:
            position = get_coordinates(form.cleaned_data['city']+', '+form.cleaned_data['address'])
            lng = None
            lat = None
            if position:
                lng = position['lng']
                lat = position['lat']
            restaurant = Restaurant.objects.create(
                name=form.cleaned_data['restaurant_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                n_places=form.cleaned_data['n_places'],
                booking_duration=form.cleaned_data['booking_duration'],
                longitude=lng,
                latitude=lat,
            )
            for service in form.cleaned_data['services']:
                restaurant.services.add(Service.objects.get(id=service))
            for kitchen_type in form.cleaned_data['kitchen_types']:
                restaurant.kitchen_types.add(KitchenType.objects.get(id=kitchen_type))
            user.restaurant_information = restaurant
            user.save()
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('booking:index'))


@login_required
@user_passes_test(User.is_restaurant)
def count_restaurant_bookings(request):
    if request.is_ajax():
        response = {}
        try:
            time = timezone.make_aware(datetime.strptime(request.POST['time'], '%Y-%m-%d-%H-%M-%S'),
                                       timezone.get_current_timezone())
            response['occupied_places'] = count_bookings(request.POST['restaurant_id'], time)
            response['result'] = 'success'
        except (User.DoesNotExist, KeyError):
            response['result'] = 'error'
        return JsonResponse(response)
    else:
        raise Http404
