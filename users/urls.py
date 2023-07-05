from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('UserLogin/', views.login, name='login'),

]
