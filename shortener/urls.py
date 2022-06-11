from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('register/', views.RegistrationView.as_view(), name='register'),
]