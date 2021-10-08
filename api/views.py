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
    if PostUser.objects.filter(api_token=api_key):
        date_format = '%Y-%m-%d'
        try:
            date_from = datetime.datetime.strptime(from_date, date_format)
            date_to = datetime.datetime.strptime(to_date, date_format)
            date_to = date_to + datetime.timedelta(days=1)
            to_date = date_to.strftime(date_format)
        except ValueError as e:
            data = {
                'value error': f'date format must be :{date_format}',
            }
            return Response(data, status=HTTP_400_BAD_REQUEST)

        posts = LikeReaction.objects.filter(reacted__range=[from_date, to_date])
        serializer = ReactionSerializer(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    else:
        raise PermissionDenied('invalid api token')
