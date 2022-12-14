from django.urls import path

from . import views

app_name = 'competitions'

urlpatterns = [
    path('', views.CompetitionListView.as_view(), name='competition_list'),
    path('<int:cpk>/team/<int:tpk>/', views.CompetitionTeamDetailView.as_view(), name='competition_team_detail'),
    path('<int:pk>/', views.CompetitionDetailView.as_view(), name='competition_detail'),
    path('create/', views.CompetitionCreateView.as_view(), name='competition_create'),
    path('edit/<int:pk>/', views.CompetitionUpdateView.as_view(), name='competition_edit'),
    path('schedule/<int:pk>/', views.MatchScheduleView.as_view(), name='schedule_list'),
    path('table/<int:pk>/', views.CompetitionTableLeagueView.as_view(), name='table'),
    path('add/match/', views.MatchCreateView.as_view(), name='add_match'),
    path('edit/match/<int:pk>/', views.MatchUpdateView.as_view(), name='edit_match'),
    path('delete/match/<int:pk>/', views.MatchDeleteView.as_view(), name='delete_match'),
    path('delete/<int:pk>/', views.CompetitionDeleteView.as_view(), name='competition_delete'),
]
