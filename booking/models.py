from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from user_management.models import User, Restaurant


class Booking(models.Model):
    STATES = (
        (0, 'In attesa'),
        (1, 'Confermata'),
    )

    client = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='bookings', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    n_places = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    state = models.PositiveSmallIntegerField(choices=STATES)

    def calculate_end_time(self):
        return self.start_time + timedelta(minutes=self.restaurant.booking_duration)

    def clean(self):
        super(Booking, self).clean()

        # if self.start_time < timezone.make_aware(datetime.now(), timezone.get_current_timezone()):
        #     raise ValidationError('Start time must be later than now.')

        if self.end_time and self.end_time <= self.start_time:
            raise ValidationError('End time must be later than start time.')
