from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('likes/analytics/<str:from_date>/<str:to_date>/<str:api_key>', views.get_reaction_statistic, name='get_likes'),
]
