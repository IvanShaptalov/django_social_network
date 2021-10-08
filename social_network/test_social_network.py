from django.test import TestCase
from django.test import Client

# Create your tests here.
# todo test view function, test serializer
from rest_framework import status


class TestViews(TestCase):
    def setUp(self) -> Client:
        self.c = Client()
        self.index = ''
        self.login = '/accounts/login/'
        self.register_done = '/accounts/register/done/'
        self.register = '/accounts/register/'
        self.post_add = '/accounts/profile/post_add/'
        self.get_token = '/accounts/profile/personal_token/'
        self.profile = '/accounts/profile/'

    def test_index(self):
        response = self.c.get(self.index)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'index page found')

    def test_login(self):
        response = self.c.get(self.login)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'login page not found')

    def test_register(self):
        response = self.c.get(self.register)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'register page not found')

    def test_get_token_no_login(self):
        response = self.c.get(self.get_token)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND, f'not redirected from token page to login')

    def test_register_done(self):
        response = self.c.get(self.register_done)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'not found register page')

    def test_post_add_no_login(self):
        response = self.c.get(self.post_add)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND, f'not redirected from post to login')

    def test_profile_no_login(self):
        response = self.c.get(self.profile)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND, f'not redirected from profile to login')


class TestConfig(TestCase):
    def test_configuration_file(self):
        try:
            from django_site import settings, project_config
            variables = [item for item in dir(settings) if not item.startswith("__")]
            variables_config = [item for item in dir(project_config) if not item.startswith("__")]
            for var in variables:
                attr = getattr(settings, var)
                self.assertIsNotNone(attr, f'attr {var} is {attr} in settings.py')
            for var in variables_config:
                attr = getattr(project_config, var)
                self.assertIsNotNone(attr, f'attr {var} is {attr} in project_config.py')

        except Exception as e:
            print(e)
            self.fail('e')

# class TestModels(TestCase):
#     def setUp(self) -> None: