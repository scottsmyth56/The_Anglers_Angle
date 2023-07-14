from . import views
from django.urls import path

urlpatterns = [
    path('post-lists', views.PostList.as_view(), name='post-list'),
    path('', views.index.as_view(), name='index'),
    path('add-post/', views.addPost.as_view(), name='addPost'),
    path('edit-post/<int:pk>', views.editPost.as_view(), name='editPost'),
    path('delete-post/<int:pk>', views.deletePost.as_view(), name='deletePost'),
    path('post/<int:pk>/', views.viewPost.as_view(), name='viewPost'),
    path('likePost/<int:pk>/', views.likePost.as_view(), name='likePost'),
    path('unlikePost/<int:pk>/', views.unlikePost.as_view(), name='unlikePost'),
    path('addComment/<int:pk>/', views.addComment.as_view(), name='addComment'),

]
