from . import views
from django.urls import path

urlpatterns = [
    path('groups', views.viewGroups.as_view(), name='groups'),
    path('add-group/', views.addGroup.as_view(), name='addGroup'),
    path('group/<int:pk>/', views.viewGroup.as_view(),
         name='viewGroup'),
]
