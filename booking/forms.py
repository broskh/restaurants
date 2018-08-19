from django import forms

from user_management.models import Service, KitchenType
from .models import Booking


class BookingForm (forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'n_places', 'state']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.DateTimeInput()
        self.fields['start_time'].input_formats = ['%Y-%m-%d-%H-%M-%S']
        self.fields['n_places'].widget = forms.NumberInput(attrs={
            'class': 'form-control'})
        self.fields['state'].widget = forms.Select()
        self.fields['state'].choices = Booking.STATES


class SearchForm (forms.Form):
    site = forms.CharField(max_length=300,
                           widget=forms.TextInput(attrs={'class':'form-control',
                                                         'placeholder':'Luogo ',
                                                         'onfocus':"this.placeholder = ''",
                                                         'onblur':"this.placeholder = 'Luogo '"
                                                         }))
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control date-picker',
                                                         'placeholder':'Data ',
                                                         'onfocus':"this.placeholder = ''",
                                                         'onblur':"this.placeholder = 'Data '"
                                                         }))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control time-picker',
                                                         'placeholder':'Ora ',
                                                         'onfocus':"this.placeholder = ''",
                                                         'onblur':"this.placeholder = 'Ora '"
                                                         }))
    n_clients = forms.IntegerField(min_value=1,
                                    widget=forms.NumberInput(attrs={'class':'form-control',
                                                                     'placeholder':'N° Clienti ',
                                                                     'onfocus':"this.placeholder = ''",
                                                                     'onblur':"this.placeholder = 'N° Clienti '"
                                                                     }))
    services = forms.MultipleChoiceField(
                    choices = Service.objects.values_list('id', 'value'),
                    widget = forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'
                                                                  }))
    kitchenTypes = forms.MultipleChoiceField(
                        choices = KitchenType.objects.values_list('id', 'value'),
                        widget  = forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'
                                                                  }))
