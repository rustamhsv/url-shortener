from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from shortener.models import URL


class RegistrationViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/shortener/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_correct_template(self):
        response = self.client.get('/shortener/register/')

        # Check if we used correct template
        self.assertTemplateUsed(response, 'register.html')


class URLShortenerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user
        test_user = User.objects.create_user('tester', 'tester@test.com', 'verystrongpassword')

        # store in mock database
        URL.objects.create(long_URL='https://www.britannica.com/topic/history',
                           short_URL='127.0.0.1:8000/G',
                           user=test_user)

    def test_view_url_exists_at_desired_location(self):
        # login the test user - because the page is login required
        self.client.login(username='tester', password='verystrongpassword')
        response = self.client.get('/shortener/shorten/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login(self):
        response = self.client.get('/shortener/shorten/')

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?login=/shortener/shorten/')


class MyUrlsListViewTest(TestCase):
    def setUp(self) -> None:
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_superuser('tester', 'tester@test.com', 'verystrongpassword')

        # login the test user - because the page is login required
        self.client.login(username='tester', password='verystrongpassword')

        URL.objects.create(long_URL='https://www.britannica.com/topic/history',
                           short_URL='127.0.0.1:8000/G',
                           user=test_user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/shortener/my-urls/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        response = self.client.get('/shortener/my-urls/')

        # Check if we used correct template
        self.assertTemplateUsed(response, 'shortener/my_url_list.html')


class RedirectURLViewTest(TestCase):
    def setUp(self) -> None:
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_superuser('tester', 'tester@test.com', 'verystrongpassword')

        URL.objects.create(long_URL='https://www.britannica.com/topic/history',
                           short_URL='127.0.0.1:8000/G',
                           user=test_user)

    def test_redirect_from_short_to_long_url(self):
        response = self.client.get('/G', follow=True)
        self.assertEqual(response.status_code, 200)


class HomePageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/shortener/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
