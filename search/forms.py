from django import forms
from .models import Service, KitchenType


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