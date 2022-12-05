from django.shortcuts import render

# Create your views here.
from django import views
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


