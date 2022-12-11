from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamsListView.as_view(), name='teams_list'),
    path('create', views.TeamCreateView.as_view(), name='team_add'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('edit/<int:pk>/', views.TeamUpdateView.as_view(), name='team_edit'),
    path('delete/<int:pk>/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('delete/playerforteam/<int:pk>/', views.DeletePlayerForTeamView.as_view(), name='delete_player_for_team'),
    path('add/player/', views.AddPlayerToTeam.as_view(), name='add_player_to_team'),



]