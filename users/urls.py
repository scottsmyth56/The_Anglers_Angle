from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('UserLogin/', views.login, name='login'),
    path('UserLogout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('edit_profile/', views.edit_profile, name='editProfile'),
    path('profile/<str:username>/', views.view_profile, name='profile'),

]
