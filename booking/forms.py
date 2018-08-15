from django import forms
from .models import Booking


class BookingForm (forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['start_time', 'n_places']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.DateTimeInput()
        self.fields['start_time'].input_formats = ['%Y-%m-%d-%H-%M-%S']
        self.fields['n_places'].widget = forms.NumberInput(attrs={
            'class': 'form-control'})
