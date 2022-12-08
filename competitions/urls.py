from django.urls import path

from . import views

app_name = 'competitions'

urlpatterns = [
    path('', views.CompetitionListView.as_view(), name='competition_list'),
    path('<int:pk>/', views.CompetitionDetailView.as_view(), name='competition_detail'),
    path('create/', views.CompetitionCreateView.as_view(), name='competition_create'),
    path('edit/<int:pk>/', views.CompetitionUpdateView.as_view(), name='competition_edit'),
    path('delete/<int:pk>/', views.CompetitionDeleteView.as_view(), name='competition_delete'),

]
