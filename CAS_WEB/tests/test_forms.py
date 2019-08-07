from django.test import TestCase

from cas.forms import *
from cas.models import *


class LoginFormTest(TestCase):
    def test_login_form_success(self):
        data = {
            "username": "yueqi",
            "password": "yueqi"
        }
        form = LoginForm(data=data)
        form.is_valid()
        self.assertFalse(form.errors)

    def test_login_form_failure(self):
        data = {
            "username": "yueqi",
            "password": "wrongpassword"
        }
        form = LoginForm(data=data)
        form.is_valid()
        self.assertTrue(form.errors)


class RegistrationFormTest(TestCase):
    def test_registration_form_success(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "username": "janedoe",
            "password1": "password",
            "password2": "password",
        }
        form = RegistrationForm(data=data)
        form.is_valid()
        self.assertFalse(form.errors)

    def test_registration_form_password_not_matching(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "username": "janedoe",
            "password1": "password",
            "password2": "password_1",
        }
        form = RegistrationForm(data=data)
        form.is_valid()
        self.assertTrue(form.errors)

    def test_registration_form_duplicated_users(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "username": "admin",
            "password1": "password",
            "password2": "password",
        }
        form = RegistrationForm(data=data)
        form.is_valid()
        self.assertTrue(form.errors)
