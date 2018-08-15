from time import strftime

from django import forms
from .models import User
from search.models import Restaurant, KitchenType, Service


class UserInfoForm (forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control'})
        self.fields['confirm_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control'})


class RestaurantInfoForm (forms.ModelForm):
    load_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                         'class':'custom-file-input'}),
                                  required=False)
    remove_images = forms.Field(widget=forms.HiddenInput(), required=False)
    add_categories = forms.Field(widget=forms.HiddenInput(), required=False)
    remove_categories = forms.Field(widget=forms.HiddenInput(), required=False)
    add_voices = forms.Field(widget=forms.HiddenInput(), required=False)
    remove_voices = forms.Field(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Restaurant
        fields = ['name', 'kitchen_types', 'services', 'city', 'address', 'n_places', 'booking_duration']

    def __init__(self, *args, **kwargs):
        super(RestaurantInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['kitchen_types'].widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'})
        self.fields['kitchen_types'].choices = KitchenType.objects.values_list('id', 'value')
        self.fields['services'].widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'})
        self.fields['services'].choices = Service.objects.values_list('id', 'value')
        self.fields['city'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs={
            'class': 'form-control'})
        self.fields['n_places'].widget = forms.NumberInput(attrs={
            'class': 'form-control'})
        self.fields['booking_duration'].widget = forms.NumberInput(attrs={
            'class': 'form-control'})


class RegistrationForm (forms.Form):
    USER_TYPES=[User.TYPES[1],
                User.TYPES[2]]

    username = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={
            'class': 'form-control'}),
            required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}),
            required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control'}),
            required=True)
    type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect(attrs={
            'class': 'custom-control-input'}),
            initial=USER_TYPES[0][0],
            required=True)
    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False)
    kitchen_types = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'}),
            choices=KitchenType.objects.values_list('id', 'value'),
            required=False)
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'}),
            choices=Service.objects.values_list('id', 'value'),
            required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control'}),
            required=False)
    n_places = forms.CharField(widget=forms.NumberInput(attrs={
            'class': 'form-control'}),
            required=False)
    booking_duration = forms.CharField(widget=forms.NumberInput(attrs={
            'class': 'form-control'}),
            required=False)

    # name = models.CharField(max_length=250)
    # kitchenTypes = models.ManyToManyField(KitchenType)
    # services = models.ManyToManyField(Service)
    # city = models.CharField(max_length=300)
    # address = models.CharField(max_length=300)
    # nPlaces = models.PositiveIntegerField(default=1)
    # bookingDuration = models.PositiveIntegerField(default=120)