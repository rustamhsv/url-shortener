from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from shortener.forms import RegistrationForm


def index(request):
    # Home page view
    return render(request, 'index.html')


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # redirect to login after successful registration
    form_class = RegistrationForm
    success_message = 'Your profile was created successfully'
