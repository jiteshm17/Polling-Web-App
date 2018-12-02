from django import forms
#from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class login_form(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

class editprofile(UserChangeForm):
    class Meta:
        model=User
        fields = (
            'first_name',
            'last_name',
            'password',
        )

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    """full_name = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    male='M'
    female='F'
    category = (
        (male,'Male'),
        (female,'Female'),
    )
    gender = forms.Charfield(
        max_length =1,
        choices = category,
        default=male,

    )"""
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )
