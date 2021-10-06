from django.urls import path

from social_network import views

app_name = 'social_network'

urlpatterns = [
    path('', views.index, name='index'),
    # Login
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.UserLogoutView.as_view(), name='logout'),
    # Registration
    path('accounts/register/activate/<str:sign>/', views.index, name='register_activate'),
    path('accounts/register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    # Add and edit post
    path('accounts/profile/post_add/', views.profile_post_add, name='profile_post_add'),
    path('accounts/profile/post_edit/<int:pk>/', views.profile_post_change, name='profile_post_edit'),
    path('accounts/profile/', views.index, name='profile'),

]
