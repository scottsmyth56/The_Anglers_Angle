from . import views
from django.urls import path

urlpatterns = [
    path('competitions', views.viewCompetitions.as_view(), name='competitions'),
    path('add-competition/', views.addCompetition.as_view(), name='addCompetition'),
    path('competition/<int:pk>/', views.viewCompetitionDetailed.as_view(),
         name='viewCompetitionDetailed'),
    # path('edit-post/<int:pk>', views.editPost.as_view(), name='editPost'),
    # path('delete-post/<int:pk>', views.deletePost.as_view(), name='deletePost'),

]
