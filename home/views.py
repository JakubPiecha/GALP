from django.shortcuts import render

# Create your views here.
from django import views
from django.views.generic import TemplateView


class HomeView(TemplateView):
    '''
    This view is used to display the home page
    '''
    template_name = 'home/home.html'
