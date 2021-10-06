from django.apps import AppConfig
from django.dispatch import Signal

from social_network.utilities import send_activation_notification


class SocialNetworkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_network'


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registered = Signal(providing_args=['instance'])
user_registered.connect(user_registered_dispatcher)
