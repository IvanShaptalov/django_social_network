# todonext write last user request middleware
import datetime

from django.utils.timezone import now

from social_network.models import PostUser


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print('last request', datetime.datetime.now())
            PostUser.objects.filter(pk=request.user.pk).update(date_last_request=now())
        response = self.get_response(request)
        return response
