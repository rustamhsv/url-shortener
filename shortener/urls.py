from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten/', views.URLShortenerView.as_view(), name='shorten'),
]

urlpatterns += [
    path('register/', views.RegistrationView.as_view(), name='register'),
]
