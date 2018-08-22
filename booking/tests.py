from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from booking.models import Booking
from restaurants.utils import get_coordinates
from user_management.models import Restaurant, User


class BookingMethodsTests(TestCase):
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
        self.booking = Booking(
            client=self.client_user,
            restaurant=self.restaurant,
            n_places=2,
            start_time=timezone.make_aware(datetime.now(), timezone.get_current_timezone()).replace(microsecond=0),
            state=Booking.STATES[0][0]
        )
        self.booking.end_time = self.booking.calculate_end_time()

    def test_end_is_after_start(self):
        self.assertEqual(self.booking.end_time <= self.booking.start_time, False)


class IndexWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:index')
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
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Logout')

    def test_client_logged(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gestione prenotazioni')

    def test_restaurant_logged(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gestione ristorante')


class ResultsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:search_results')
        self.client = Client()
        self.datetime = timezone.make_aware(datetime.now(), timezone.get_current_timezone()).replace(microsecond=0)
        self.restaurant1 = Restaurant(
            name='da mario',
            city='vignola',
            address='via baracchini, 95',
            n_places=50,
            booking_duration=120
        )
        restaurant_position = get_coordinates(self.restaurant1.city + ', ' + self.restaurant1.address)
        self.restaurant1.latitude = restaurant_position['lat']
        self.restaurant1.longitude = restaurant_position['lng']
        self.restaurant2 = Restaurant(
            name='da paolo',
            city='san cesario sul panaro',
            address='via della meccanica',
            n_places=80,
            booking_duration=90
        )
        restaurant_position = get_coordinates(self.restaurant2.city + ', ' + self.restaurant2.address)
        self.restaurant2.latitude = restaurant_position['lat']
        self.restaurant2.longitude = restaurant_position['lng']
        self.restaurant3 = Restaurant(
            name='da paolo',
            city='alba adriatica',
            address='via pompeo',
            n_places=120,
            booking_duration=150
        )
        restaurant_position = get_coordinates(self.restaurant3.city + ', ' + self.restaurant3.address)
        self.restaurant3.latitude = restaurant_position['lat']
        self.restaurant3.longitude = restaurant_position['lng']

    def test_with_results(self):
        self.restaurant1.save()
        self.restaurant2.save()
        self.restaurant3.save()
        data = {
            'site': 'savignano sul panaro',
            'date': self.datetime.strftime("%d/%m/%Y"),
            'time': self.datetime.strftime("%H:%M"),
            'n_clients': 2
        }

        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['restaurants_available'], [])

    def test_without_results(self):
        data = {
            'site': 'savignano sul panaro',
            'date': self.datetime.strftime("%d/%m/%Y"),
            'time': self.datetime.strftime("%H:%M"),
            'n_clients': 2
        }

        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['restaurants_available'], [])
        self.assertEqual(response.context['restaurants_busy'], [])

    def test_ordered_results_and_closer_or_equal_than_50_km(self):
        self.restaurant1.save()
        self.restaurant2.save()
        self.restaurant3.save()
        data = {
            'site': 'savignano sul panaro',
            'date': self.datetime.strftime("%d/%m/%Y"),
            'time': self.datetime.strftime("%H:%M"),
            'n_clients': 2
        }

        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['restaurants_available'][0]['restaurant'], self.restaurant1)
        self.assertEqual(response.context['restaurants_available'][1]['restaurant'], self.restaurant2)
        self.assertEqual(len(response.context['restaurants_available']), 2)


class RestaurantBookingsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:restaurant_bookings')
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
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_restaurant_logged_with_restaurant_information(self):
        self.restaurant_user.restaurant_information = self.restaurant
        self.restaurant_user.save()
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ClientBookingsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:client_bookings')
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

    def test_restaurant_logged(self):
        self.restaurant_user.client_information = self.restaurant
        self.restaurant_user.save()
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged_without_results(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['booking_list'], [])

    def test_client_logged_with_results(self):
        self.booking.save()
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['booking_list'][0], self.booking)

    def test_booking_before_now(self):
        self.booking.start_time = self.datetime - timedelta(minutes=1)
        self.booking.save()
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['booking_list'], [])


class DeleteBookingsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:delete_booking')
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

    def test_restaurant_logged(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged_ajax_call(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.post(self.url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_client_logged_no_ajax_call(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 404)

    def test_client_logged_ajax_call_with_booking(self):
        self.booking.save()
        self.client.login(username=self.client_user.username, password=self.password)

        data = {
            'id': self.booking.id
        }
        data_result = {
            'result': 'success'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)

    def test_client_logged_ajax_call_without_booking(self):
        self.client.login(username=self.client_user.username, password=self.password)

        data = {
            'id': 0
        }
        data_result = {
            'result': 'error'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)


class EditBookingsWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:edit_booking')
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

    def test_restaurant_logged(self):
        self.client.login(username=self.restaurant_user.username, password=self.password)

        response = self.client.get(self.url)
        expected_url = reverse('login') + '?next=' + self.url
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_client_logged_ajax_call(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.post(self.url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_client_logged_no_ajax_call(self):
        self.client.login(username=self.client_user.username, password=self.password)

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 404)

    def test_client_logged_ajax_call_with_booking(self):
        self.booking.save()
        self.client.login(username=self.client_user.username, password=self.password)

        data = {
            'id': self.booking.id,
            'n_places': 10,
            'start_time': (self.datetime + timedelta(minutes=30)).strftime("%Y-%m-%d-%H-%M-%S"),
            'state': Booking.STATES[0][0]
        }
        data_result = {
            'result': 'success'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)

    def test_client_logged_ajax_call_without_booking(self):
        self.client.login(username=self.client_user.username, password=self.password)

        data = {
            'id': 0,
            'n_places': 10,
            'start_time': (self.datetime + timedelta(minutes=30)).strftime("%Y-%m-%d-%H-%M-%S"),
            'state': Booking.STATES[0][0]
        }
        data_result = {
            'result': 'error'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)


class CheckAvailabilityWiewTests(TestCase):
    def setUp(self):
        self.url = reverse('booking:check_availability')
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

    def test_client_logged_ajax_call(self):

        response = self.client.post(self.url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_client_logged_no_ajax_call(self):

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 404)

    def test_client_logged_ajax_call_with_data(self):
        self.booking.save()
        self.client.login(username=self.client_user.username, password=self.password)

        data = {
            'restaurant_id': self.restaurant.id,
            'n_places': 10,
            'start_time': self.datetime.strftime("%Y-%m-%d-%H-%M-%S")
        }
        data_result = {
            'result': 'success',
            'state': Booking.STATES[1][0]
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)

    def test_client_logged_ajax_call_without_data(self):

        data = {
            'restaurant_id': 0,
            'n_places': 10,
            'start_time': self.datetime.strftime("%Y-%m-%d-%H-%M-%S")
        }
        data_result = {
            'result': 'error'
        }
        response = self.client.post(self.url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), data_result)
