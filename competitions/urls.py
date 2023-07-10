from . import views
from django.urls import path

urlpatterns = [
    # path('competitiond', views.competitions.as_view(), name='competitions'),
    path('add-competition/', views.addCompetition.as_view(), name='addCompetition'),
    # path('edit-post/<int:pk>', views.editPost.as_view(), name='editPost'),
    # path('delete-post/<int:pk>', views.deletePost.as_view(), name='deletePost'),
    # path('post/<int:pk>/', views.viewPost.as_view(), name='viewPost'),
]
