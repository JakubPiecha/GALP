from django.urls import path

from . import views

app_name = 'players'

urlpatterns = [
    path('', views.PlayerListView.as_view(), name='player_list'),
    path('create/', views.PlayerCreateView.as_view(), name='player_add'),
    path('<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('edit/<int:pk>/', views.PlayerUpdateView.as_view(), name='player_edit'),
    path('delete/<int:pk>/', views.PlayerDeleteView.as_view(), name='player_delete'),

]
