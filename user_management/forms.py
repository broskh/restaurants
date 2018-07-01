from django import forms
from .models import User


class ClientInfoForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', ]