from django.urls import path

from social_network import views

app_name = 'social_network'

urlpatterns = [
    # Login
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.UserLogoutView.as_view(), name='logout'),
    # Registration
    path('accounts/register/activate/<str:sign>/', views.user_activate, name='register_activate'),
    path('accounts/register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    # Add and edit post
    path('accounts/profile/post_add/', views.profile_post_add, name='profile_post_add'),
    path('accounts/profile/post_edit/<int:pk>/', views.profile_post_change, name='profile_post_edit'),
    # Api token
    path('accounts/profile/personal_token/', views.api_token, name='profile_api_token'),

    path('accounts/profile/', views.profile_posts, name='profile'),
    # Post reaction
    path('reaction/<int:pk>', views.handle_reaction, name='handle_reaction'),
    path('', views.index, name='index'),

]
