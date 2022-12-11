from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Player
# Create your views here.


class PlayerListView(ListView):
    model = Player
    template_name = 'players/players_list.html'
    context_object_name = 'players'


class PlayerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Player
    fields = ('fullname', 'date_of_birth')
    template_name = 'players/players_add.html'
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'player.add_player'


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'


class PlayerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Player
    fields = ('fullname', 'date_of_birth')
    template_name = 'players/players_edit.html'
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'player.change_player'


class PlayerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Player
    success_url = reverse_lazy('players:player_list')
    login_url = reverse_lazy('players:player_list')
    permission_required = 'player.delete_player'
