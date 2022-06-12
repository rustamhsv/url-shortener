from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shorten/', views.URLShortenerView.as_view(), name='shorten'),
    path('my-urls/', views.MyUrlsListView.as_view(), name='my-urls'),
]

urlpatterns += [
    path('register/', views.RegistrationView.as_view(), name='register'),
]
