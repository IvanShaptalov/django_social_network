import datetime

from django.shortcuts import render
from django.core.exceptions import PermissionDenied

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from api.serializers import ReactionSerializer
from social_network.models import PostUser, LikeReaction


@api_view(['GET'])
def get_reaction_statistic(request, from_date, to_date, api_key):
    """api to give users reaction aggregated by day
     from_date - start aggregate day, valid date: 2021-04-17
     to_date - end date
     api_key - user api key"""

    # if user api is not valid show forbidden page
    if PostUser.objects.filter(api_token=api_key):
        date_format = '%Y-%m-%d'
        # if user have api key
        # try convert data from string and add 1 day to
        # upper_bound date to include current day
        try:
            date_from = datetime.datetime.strptime(from_date, date_format)
            date_to = datetime.datetime.strptime(to_date, date_format)
            date_to = date_to + datetime.timedelta(days=1)
            to_date = date_to.strftime(date_format)
            if date_from > date_to:
                # if start day bigger than end_date raise error
                raise ValueError()
        except ValueError as e:
            data = {
                'value error': f'date format must be :{date_format}',
            }
            # return response that data is not valid
            return Response(data, status=HTTP_400_BAD_REQUEST)
        # if data valid - add posts, aggregated by this diapason
        # serialize and send to user
        posts = LikeReaction.objects.filter(reacted__range=[from_date, to_date])
        serializer = ReactionSerializer(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    else:
        raise PermissionDenied('invalid api token')
