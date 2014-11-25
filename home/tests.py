from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client


class HomePageTest(TestCase):

    def setup(self):
        setup_test_environment()
        self.client = Client()

    def test_home_page(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context['customers']), 5)
