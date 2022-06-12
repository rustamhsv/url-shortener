from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shortener.models import URL


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Override default help text strings with empty strings
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    email = forms.EmailField(required=True)

    class Meta:
        # use 4 fields in the registration process
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class URLShortenerForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['long_URL']
