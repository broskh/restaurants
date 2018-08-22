from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from .models import User
from .models import Restaurant, KitchenType, Service


class UserInfoForm (forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 150})
        self.fields['username'].required = True
        self.fields['username'].label = 'Username:'
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 30})
        self.fields['first_name'].required = True
        self.fields['first_name'].label = 'Nome:'
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 30})
        self.fields['last_name'].required = True
        self.fields['last_name'].label = 'Cognome:'
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'max_length': 254})
        self.fields['email'].required = True
        self.fields['email'].label = 'E-mail:'
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'max_length': 128})
        self.fields['password'].required = True
        self.fields['password'].label = 'Password:'
        self.fields['confirm_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'max_length': 128})
        self.fields['confirm_password'].required = True
        self.fields['confirm_password'].label = 'Conferma password:'

    def clean(self):
        cleaned_data = super(UserInfoForm, self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if len(password) < 8:
            raise ValidationError('Password too short')
        if not confirm_password == password:
            raise ValidationError("Password does not match")
        return cleaned_data


class RestaurantInfoForm (forms.ModelForm):
    load_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                         'class': 'custom-file-input'}),
                                  required=False,
                                  label='Carica foto:')
    remove_images = forms.Field(widget=forms.HiddenInput(), required=False)
    add_categories = forms.Field(widget=forms.HiddenInput(), required=False, label='Menù:')
    remove_categories = forms.Field(widget=forms.HiddenInput(), required=False)
    add_voices = forms.Field(widget=forms.HiddenInput(), required=False)
    remove_voices = forms.Field(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'kitchen_types', 'services', 'city', 'address', 'n_places', 'booking_duration']

    def __init__(self, *args, **kwargs):
        super(RestaurantInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 200})
        self.fields['name'].required = True
        self.fields['name'].label = 'Nome:'
        self.fields['kitchen_types'].widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'})
        self.fields['kitchen_types'].choices = KitchenType.objects.values_list('id', 'value')
        self.fields['kitchen_types'].required = True
        self.fields['kitchen_types'].label = 'Tipi di cucina:'
        self.fields['services'].widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'})
        self.fields['services'].choices = Service.objects.values_list('id', 'value')
        self.fields['services'].required = True
        self.fields['services'].label = 'Servizi:'
        self.fields['city'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 150})
        self.fields['city'].required = True
        self.fields['city'].label = 'Città:'
        self.fields['address'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'max_length': 150})
        self.fields['address'].required = True
        self.fields['address'].label = 'Indirizzo:'
        self.fields['n_places'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1})
        self.fields['n_places'].required = True
        self.fields['n_places'].label = 'Nº posti:'
        self.fields['booking_duration'].widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1})
        self.fields['booking_duration'].required = True
        self.fields['booking_duration'].label = 'Durata (in minuti):'


class RegistrationForm (UserInfoForm):

    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False,
            max_length=200,
            label='Nome del ristorante:')
    kitchen_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'}),
            choices=KitchenType.objects.values_list('id', 'value'),
            required=False,
            label='Tipi di cucina:')
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'}),
            choices=Service.objects.values_list('id', 'value'),
            required=False,
            label='Serivizi:')
    city = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False,
            max_length=150,
            label='Città:')
    address = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False,
            max_length=150,
            label='Indirizzo:')
    n_places = forms.CharField(widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1}),
            required=False,
            label='Nº posti:')
    booking_duration = forms.CharField(widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1}),
            required=False,
            label='Durata prenotazione (in minuti):')

    class Meta(UserInfoForm.Meta):
        fields = UserInfoForm.Meta.fields + ['user_type']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['user_type'].widget = forms.RadioSelect(attrs={'class': 'custom-control-input'})
        self.fields['user_type'].initial = User.TYPES[0][0]
        self.fields['user_type'].choices = User.TYPES
        self.fields['user_type'].required = True
        self.fields['user_type'].label = 'Tipo di utente:'


class UserChangeFormAdmin(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
