from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from booking.models import Booking
from restaurants.utils import get_coordinates
from user_management.models import Restaurant, User


class UserMethodsTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='da mario',
            city='vignola',
            address='via baracchini, 95',
            n_places=50,
            booking_duration=120
        )
        self.client_user = User.objects.create(
            first_name='paolo',
            last_name='verdi',
            email='paolo.verdi@mail.com',
            username='paolo1',
            user_type=User.TYPES[0][0]
        )
        self.client_user.set_password('password')
        self.restaurant_user = User.objects.create(
            first_name='mario',
            last_name='rossi',
            email='mario.rossi@mail.com',
            username='mario1',
            user_type=User.TYPES[1][0],
            restaurant_information=self.restaurant
        )
        self.restaurant_user.set_password('password')
        restaurant_position = get_coordinates(self.restaurant.city + ', ' + self.restaurant.address)
        self.restaurant.latitude = restaurant_position['lat']
        self.restaurant.longitude = restaurant_position['lng']

    def test_restaurant_is_not_client(self):
        for user in User.objects.all():
            if user.is_restaurant():
                self.assertEqual(user.is_client(), False)

    def test_client_is_not_restaurant(self):
        for user in User.objects.all():
            if user.is_client():
                self.assertEqual(user.is_restaurant(), False)

    def test_min_distance_positive(self):
        distance = self.restaurant.get_distance_from_position(
            get_coordinates(self.restaurant.city + ', ' + self.restaurant.address))
        self.assertEqual(distance < 0, False)


class UserInfoWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('user_management:user_info')
        self.client = Client()
        self.password = 'password'
        self.restaurant = Restaurant.objects.create(
            name='da mario',
            city='vignola',
            address='via baracchini, 95',
            n_places=50,
            booking_duration=120
        )
        restaurant_position = get_coordinates(self.restaurant.city + ', ' + self.restaurant.address)
        self.restaurant.latitude = restaurant_position['lat']
        self.restaurant.longitude = restaurant_position['lng']
        self.restaurant.save()
        self.client_user = User.objects.create(
            first_name='paolo',
            last_name='verdi',
            email='paolo.verdi@mail.com',
            username='paolo1',
            user_type=User.TYPES[0][0]
        )
        self.client_user.set_password(self.password)
        self.client_user.save()
        self.restaurant_user = User.objects.create(
            first_name='mario',
            last_name='rossi',
            email='mario.rossi@mail.com',
            username='mario1',
            user_type=User.TYPES[1][0],
            restaurant_information=self.restaurant
        )
        self.restaurant_user.set_password(self.password)
        self.restaurant_user.save()

    def test_not_logged_user(self):
        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_logged(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class RestaurantInfoWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('user_management:restaurant_info')
        self.client = Client()
        self.password = 'password'
        self.restaurant = Restaurant.objects.create(
            name='da mario',
            city='vignola',
            address='via baracchini, 95',
            n_places=50,
            booking_duration=120
        )
        restaurant_position = get_coordinates(self.restaurant.city + ', ' + self.restaurant.address)
        self.restaurant.latitude = restaurant_position['lat']
        self.restaurant.longitude = restaurant_position['lng']
        self.restaurant.save()
        self.client_user = User.objects.create(
            first_name='paolo',
            last_name='verdi',
            email='paolo.verdi@mail.com',
            username='paolo1',
            user_type=User.TYPES[0][0]
        )
        self.client_user.set_password(self.password)
        self.client_user.save()
        self.restaurant_user = User.objects.create(
            first_name='mario',
            last_name='rossi',
            email='mario.rossi@mail.com',
            username='mario1',
            user_type=User.TYPES[1][0]
        )
        self.restaurant_user.set_password(self.password)
        self.restaurant_user.save()

    def test_not_logged_user(self):
        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_restaurant_logged_with_restaurant_information(self):
        self.restaurant_user.restaurant_information = self.restaurant
        self.restaurant_user.save()
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_logged_without_restaurant_information(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 404)


class CountRestourantsBookingsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('user_management:count_restaurant_bookings')
        self.client = Client()
        self.password = 'password'
        self.datetime = timezone.make_aware(datetime.now(), timezone.get_current_timezone()).replace(microsecond=0)
        self.restaurant = Restaurant.objects.create(
            name='da mario',
            city='vignola',
            address='via baracchini, 95',
            n_places=50,
            booking_duration=120
        )
        restaurant_position = get_coordinates(self.restaurant.city + ', ' + self.restaurant.address)
        self.restaurant.latitude = restaurant_position['lat']
        self.restaurant.longitude = restaurant_position['lng']
        self.restaurant.save()
        self.client_user = User.objects.create(
            first_name='paolo',
            last_name='verdi',
            email='paolo.verdi@mail.com',
            username='paolo1',
            user_type=User.TYPES[0][0]
        )
        self.client_user.set_password(self.password)
        self.client_user.save()
        self.restaurant_user = User.objects.create(
            first_name='mario',
            last_name='rossi',
            email='mario.rossi@mail.com',
            username='mario1',
            user_type=User.TYPES[1][0],
            restaurant_information=self.restaurant
        )
        self.restaurant_user.set_password(self.password)
        self.restaurant_user.save()
        self.booking = Booking(
            client=self.client_user,
            restaurant=self.restaurant,
            start_time=self.datetime,
            n_places=2,
            state=Booking.STATES[1][0]
        )
        self.booking.end_time = self.booking.calculate_end_time()

    def test_not_logged_user(self):
        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_restaurant_logged_ajax_call(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.post(self.url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_restaurant_logged_no_ajax_call(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 404)

    def test_restaurant_logged_ajax_call_with_booking(self):
        self.booking.save()
        self.client.login(username=self.restaurant_user.username, password=self.password)

        data = {
            'restaurant_id': self.restaurant.id,
            'time': self.datetime.strftime("%Y-%m-%d-%H-%M-%S")
        }
        data_result = {
            'occupied_places': self.booking.n_places,
            'result': 'success'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)

    def test_restaurant_logged_ajax_call_without_booking(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        data = {
            'restaurant_id': self.restaurant.id,
            'time': self.datetime.strftime("%Y-%m-%d-%H-%M-%S")
        }
        data_result = {
            'occupied_places': 0,
            'result': 'success'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)
