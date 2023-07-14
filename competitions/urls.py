from . import views
from django.urls import path

urlpatterns = [
    path('competitions', views.viewCompetitions.as_view(), name='competitions'),
    path('add-competition/', views.addCompetition.as_view(), name='addCompetition'),
    path('competition/<int:pk>/', views.viewCompetitionDetailed.as_view(),
         name='viewCompetitionDetailed'),
    path('enterCompetition/<int:pk>/',
         views.enterCompetition.as_view(), name='enterCompetition'),
    path('edit-competition/<int:pk>',
         views.editCompetition.as_view(), name='editCompetition'),
    path('delete-competition/<int:pk>',
         views.deleteCompetition.as_view(), name='deleteCompetition'),
]
