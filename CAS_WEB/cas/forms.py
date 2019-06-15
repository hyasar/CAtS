from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from cas.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name  = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput(attrs={'class': 'form-control'}))
    username   = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1  = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2  = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput(attrs={'class': 'form-control'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # # Customizes form validation for the username field.
    # def clean_username(self):
    #     # Confirms that the username is not already present in the
    #     # User model database.
    #
    #
    #     # We must return the cleaned data we got from the cleaned_data
    #     # dictionary
    #     return username

class ProjectForm(forms.Form):
    name = forms.CharField(max_length=100, label='Project Name',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=600,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
