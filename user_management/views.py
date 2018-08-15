import json
import os

from django.contrib.auth import login
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

from booking.models import Booking
from search.models import RestaurantImage, MenuCategory, MenuVoice
from .forms import *


class ClientInfoView(FormView):
    form_class = UserInfoForm
    template_name = 'user_management/user_info.html'

    def get_initial(self):
        initial = super(ClientInfoView, self).get_initial()
        initial['username'] = self.request.user.username
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def get_success_url(self):
        return self.request.path  # or whatever url you want to redirect to

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.set_password(form.cleaned_data['password'])
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']

        user.save()
        login(self.request, user)
        return super(ClientInfoView, self).form_valid(form)


class RestaurantInfoView(FormView):
    form_class = RestaurantInfoForm
    template_name = 'user_management/restaurant_info.html'

    def get_success_url(self):
        return self.request.path

    def get_initial(self):
        initial = super(RestaurantInfoView, self).get_initial()
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        initial['name'] = restaurant.name
        initial['city'] = restaurant.city
        initial['address'] = restaurant.address
        initial['n_places'] = restaurant.n_places
        initial['booking_duration'] = restaurant.booking_duration
        initial['services'] = restaurant.services.all().values_list('id', flat=True)
        initial['kitchen_types'] = restaurant.kitchen_types.all().values_list('id', flat=True)
        return initial

    def get_context_data(self, **kwargs):
        context = super(RestaurantInfoView, self).get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        context['restaurant'] = restaurant
        return context

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        restaurant.name = form.cleaned_data['name']
        restaurant.city = form.cleaned_data['city']
        restaurant.address = form.cleaned_data['address']
        restaurant.n_places = form.cleaned_data['n_places']
        restaurant.booking_duration = form.cleaned_data['booking_duration']
        restaurant.services.clear()
        for service in form.cleaned_data['services']:
            restaurant.services.add(Service.objects.get(id=service.id))
        restaurant.kitchen_types.clear()
        for kitchen_type in form.cleaned_data['kitchen_types']:
            restaurant.kitchen_types.add(KitchenType.objects.get(id=kitchen_type.id))
        files = self.request.FILES.getlist('load_image')
        for f in files:
            # dirname = 'media/' + strftime('%Y/%m/%d/%H/%M/%S/')
            # os.makedirs(dirname)
            # with open(dirname + f.name, 'wb+') as destination:
            #     for chunk in f.chunks():
            #         destination.write(chunk)
            RestaurantImage.objects.create(
                image=f,
                restaurant=restaurant
            )

        if form.cleaned_data['remove_images']:
            for id in form.cleaned_data['remove_images'].split(','):
                image = RestaurantImage.objects.get(id=id)
                os.remove(image.image.path)
                image.delete()

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
                        if voice['category_id']==category['id']:
                            voice['category_id'] = new_category.id

        if form.cleaned_data['remove_categories']:
            for category in form.cleaned_data['remove_categories'].split(','):
                print(category)
                MenuCategory.objects.get(id=category).delete()

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
        return super(RestaurantInfoView, self).form_valid(form)


class RestaurantBookingsView(TemplateView):
    template_name = 'user_management/restaurant_bookings.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantBookingsView, self).get_context_data(**kwargs)
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])
        context['total_places'] = restaurant.n_places
        return context


class ClientBookingsView(ListView):
    template_name = 'user_management/client_bookings.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Booking.objects.filter(client=self.request.user)
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'user_management/registration.html'
    success_url = next

    def get_success_url(self, **kwargs):
        return self.request.GET['next']

    def form_valid(self, form):
        user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type=form.cleaned_data['type']
        )
        if int(form.cleaned_data['type']) == User.TYPES[2][0]:
            restaurant=Restaurant.objects.create(
                name=form.cleaned_data['restaurant_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                n_places=form.cleaned_data['n_places'],
                booking_duration=form.cleaned_data['booking_duration'],
            )
            for service in form.cleaned_data['services']:
                restaurant.services.add(Service.objects.get(id=service))
            for kitchen_type in form.cleaned_data['kitchen_types']:
                restaurant.kitchen_types.add(KitchenType.objects.get(id=kitchen_type))
            user.restaurant_information=restaurant
            user.save()
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)
