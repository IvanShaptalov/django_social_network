from django.test import TestCase
from django.test import Client
from social_network.models import PostUser
# Create your tests here.
# todo test view function, test serializer
from rest_framework import status


class TestApi(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        user = PostUser()
        user.api_token = 'test_token_ldkafjhdi243yhOISARUY'
        user.username = 'test'
        user.email = 'test'
        user.save()
        user = PostUser.objects.first()
        self.token = user.api_token

    def test_api_permission_denied(self):
        response = self.c.get('/api/likes/analytics/2020-04-18/2021-07-18/bad_api_key')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'api key not provide security')

    def test_api_permission_accesses(self):
        response = self.c.get(f'/api/likes/analytics/2020-04-18/2021-07-18/{self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'api not pass valid key')

    def test_api_invalid_keys(self):
        response = self.c.get(f'/api/likes/analytics/2021-07-18/2020-04-18/{self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'api pass invalid data, (from date bigger that to date)')

    def test_api_invalid_keys_month(self):
        response = self.c.get(f'/api/likes/analytics/2000-70-18/2020-04-18/{self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'api pass invalid data, month - 70')
