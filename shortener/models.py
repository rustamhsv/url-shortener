from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class URL(models.Model):
    """ Model for storing urls """
    long_URL = models.CharField(max_length=10000, help_text='Enter long URL')
    short_URL = models.CharField(max_length=100, unique=True)

    # one-to-many relationship with the users [one user - many URLs]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('url-detail', args=[str(self.id)])

    def __str__(self):
        """String representation for URL model"""
        return f'URL: {self.long_URL}, shortened URL: {self.short_URL}'
