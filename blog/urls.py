from . import views
from django.urls import path

urlpatterns = [
    path('post-lists', views.PostList.as_view(), name='post-list'),
    path('', views.index.as_view(), name='index'),
]
