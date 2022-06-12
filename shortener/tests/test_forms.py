from django.contrib.auth.models import User
from django.test import TestCase
from shortener.forms import RegistrationForm


class RegistrationFormTest(TestCase):
    def test_username_field_label(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username')

    def test_username_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['username'].help_text, '')

    def test_registration_form(self):
        form_data = {'username': 'tester',
                     'email': 'tester@mail.com',
                     'password1': 'strongpass',
                     'password2': 'strongpass',
                     }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_less_than_8_chars(self):
        form_data = {'username': 'tester',
                     'email': 'tester@mail.com',
                     'password1': '6chars',
                     'password2': '6chars',
                     }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.errors["password2"][0],
                         "This password is too short. It must contain at least 8 characters.")

    def test_passwords_not_match(self):
        form_data = {'username': 'tester',
                     'email': 'tester@mail.com',
                     'password1': 'strongpass',
                     'password2': 'weakpass',
                     }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.errors["password2"][0],
                         "The two password fields didn’t match.")

    def test_wrong_email(self):
        form_data = {'username': 'tester',
                     'email': 'testermail.com',
                     'password1': 'strongpass',
                     'password2': 'strongpass',
                     }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.errors["email"][0],
                         "Enter a valid email address.")

    def test_duplicate_username(self):
        test_user = User.objects.create_superuser('tester', 'tester@test.com', 'verystrongpassword')

        form_data = {'username': 'tester',
                           'email': 'tester@mail.com',
                           'password1': 'strongpass',
                           'password2': 'strongpass',
                           }

        form = RegistrationForm(data=form_data)
        self.assertEqual(form.errors["username"][0],
                         "A user with that username already exists.")
