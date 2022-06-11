from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
import base62


# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from shortener.forms import RegistrationForm, URLShortenerForm
from shortener.models import URL


def index(request):
    # Home page view
    return render(request, 'index.html')


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # redirect to login after successful registration
    form_class = RegistrationForm
    success_message = 'Your profile was created successfully'


class URLShortenerView(LoginRequiredMixin, generic.FormView):
    model = URL
    form_class = URLShortenerForm
    success_url = '/shortener/'
    template_name = 'shortener/url_shortener.html'
    redirect_field_name = 'login'

    def form_valid(self, form):
        # get id of last entry in database
        last_id_number = URL.objects.all().count()

        # get domain address
        domain = self.request.META['HTTP_HOST']

        # encode id into base62 string
        base62_encoding = base62.encode(last_id_number)

        # generate short url
        short_url = f'{domain}/{base62_encoding}'

        # create new db entry with long url, shortened url, and currrnt user
        url = URL.objects.create(
            long_URL=form.cleaned_data['long_URL'],
            short_URL=base62_encoding,
            user=self.request.user,
        )

        # save new entry to db
        url.save()
        return super().form_valid(form)

    def get_queryset(self):
        return URL.objects.filter(user__exact=self.request.user)


def redirect_url_view(request, base62_encoding):
    # get corresponding long url for entered short url and redirect to original(long url) page
    url = URL.objects.get(short_URL__exact=base62_encoding)
    return redirect(url.long_URL)
