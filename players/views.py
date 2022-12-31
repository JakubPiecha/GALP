from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import PlayerForm
from .models import Player
# Create your views here.


class PlayerListView(ListView):
    '''
    This view is used to display the list of players
    '''
    model = Player
    template_name = 'players/players_list.html'
    context_object_name = 'players'


class PlayerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the player creating form
    '''
    form_class = PlayerForm
    template_name = 'players/players_add.html'
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'players.add_player'


class PlayerDetailView(DetailView):
    '''
    This view is used to display player details
    '''
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'


class PlayerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    View of the player editing form
    '''
    model = Player
    form_class = PlayerForm
    template_name = 'players/players_edit.html'
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'players.change_player'


class PlayerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the competition creating form
    '''
    model = Player
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'players.delete_player'
