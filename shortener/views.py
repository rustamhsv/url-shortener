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
    """Home page view"""
    return render(request, 'index.html')


class RegistrationView(SuccessMessageMixin, CreateView):
    """Class-based Registration view for creating account."""
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # redirect to login after successful registration
    form_class = RegistrationForm
    success_message = 'Your profile was created successfully'


class URLShortenerView(LoginRequiredMixin, generic.FormView):
    """View for shortening URLs. Long urls are shortened by encoding id of the corresponding entry."""
    model = URL
    form_class = URLShortenerForm
    success_url = '/shortener/shorten'  # if form submission is successful stay on the same page & show URLs
    template_name = 'shortener/url_shortener.html'
    redirect_field_name = 'login'  # if not logged-in, redirect user to login page

    def form_valid(self, form):

        # get id of last entry in database
        last_id_number = URL.objects.last().id

        # get domain address
        domain = self.request.META['HTTP_HOST']

        # encode id into base62 string
        base62_encoding = base62.encode(last_id_number)

        # generate short url from domain name and encoding string
        short_url = f'{domain}/{base62_encoding}'

        # create new db entry with long url, shortened url, and current user
        url = URL.objects.create(
            long_URL=form.cleaned_data['long_URL'],
            short_URL=short_url,
            user=self.request.user,
        )

        # save new entry to db
        url.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # get context of current view
        context = super(URLShortenerView, self).get_context_data(**kwargs)

        # get the last entry in database for current user
        url = URL.objects.filter(user__exact=self.request.user).last()

        # if user has shortened some URL then add short and long URL strings to the context dictionary
        # to show them on the current page
        if url:
            context['long_URL'] = url.long_URL
            context['short_URL'] = url.short_URL
        return context


class MyUrlsListView(LoginRequiredMixin, generic.ListView):
    """View to store history of original and shortened URLs. Can be accessed after login."""
    model = URL
    template_name = 'shortener/my_url_list.html'
    redirect_field_name = 'login'  # if not logged-in, redirect user to login page

    def get_queryset(self):
        # get the shortened urls for current user
        return URL.objects.filter(user__exact=self.request.user)


def redirect_url_view(request, base62_encoding):
    """View to redirect short URL to original webpage."""
    # get domain address
    domain = request.META['HTTP_HOST']

    # generate short url from domain name and parameter in the path
    short_url = f'{domain}/{base62_encoding}'

    try:
        # get corresponding long URL for entered short URL and redirect to original(long url) page
        url = URL.objects.get(short_URL__exact=short_url)
        return redirect(url.long_URL)
    except URL.DoesNotExist:
        # if short URL doesn't exist in db, then redirect to home page
        return render(request, 'index.html')
