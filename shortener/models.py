from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    """ Model for storing urls """
    long_URL = models.CharField(max_length=10000, help_text='Enter long URL')
    short_URL = models.CharField(max_length=100, unique=True)

    # one-to-many relationship with the users [one user - many URLs]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """String representation for URL model"""
        return f'Long URL: {self.long_URL}, Short URL: {self.short_URL}'
