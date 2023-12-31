from . import views
from django.urls import path

urlpatterns = [
    path(
        'groups',
        views.viewGroups.as_view(),
        name='groups'),
    path(
        'add-group/',
        views.addGroup.as_view(),
        name='addGroup'),
    path(
        'group/<int:pk>/',
        views.viewGroup.as_view(),
        name='viewGroup'),
    path(
        'enterGroup/<int:pk>/',
        views.enterGroup.as_view(),
        name='enterGroup'),
    path(
        'edit-group/<int:pk>',
        views.editGroup.as_view(),
        name='editGroup'),
    path(
        'delete-group/<int:pk>',
        views.deleteGroup.as_view(),
        name='deleteGroup'),
    path(
        'add-groupPost/<int:pk>',
        views.addGroupPost.as_view(),
        name='addGroupPost'),
    path(
        'edit-groupPost/<int:pk>',
        views.editGroupPost.as_view(),
        name='editGroupPost'),
    path(
        'delete-groupPost/<int:pk>',
        views.deleteGroupPost.as_view(),
        name='deleteGroupPost'),
]
