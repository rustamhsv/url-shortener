from django.contrib.auth.models import User
from django.test import TestCase

from shortener.models import URL


class URLModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_superuser('tester', 'tester@test.com', 'verystrongpassword')

        URL.objects.create(long_URL='https://www.britannica.com/topic/history',
                           short_URL='127.0.0.1:8000/G',
                           user=test_user)

    def test_long_URL_label(self):
        url = URL.objects.get(id=1)
        field_label = url._meta.get_field('long_URL').verbose_name
        self.assertEqual(field_label, 'long URL')

    def test_short_URL_label(self):
        url = URL.objects.get(id=1)
        field_label = url._meta.get_field('short_URL').verbose_name
        self.assertEqual(field_label, 'short URL')

    def test_long_URL_max_length(self):
        url = URL.objects.get(id=1)
        max_length = url._meta.get_field('long_URL').max_length
        self.assertEqual(max_length, 10000)

    def test_short_URL_max_length(self):
        url = URL.objects.get(id=1)
        max_length = url._meta.get_field('short_URL').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_long_URL_comma_short_URL(self):
        url = URL.objects.get(id=1)
        expected_object_name = f'Long URL: {url.long_URL}, Short URL: {url.short_URL}'
        self.assertEqual(str(url), expected_object_name)
