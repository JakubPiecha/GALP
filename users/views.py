from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from users.forms import CustomUserCreationForm


# Create your views here.

class RegistrationUserView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'
