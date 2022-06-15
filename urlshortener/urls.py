"""urlshortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shortener/', include('shortener.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='shortener/', permanent=True)),
]

# add authentication paths
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# add redirection path - from shortened url to original url
urlpatterns += [
    path('<str:base62_encoding>', views.redirect_url_view, name='redirect-url'),
]

