from django.views.generic import TemplateView

from competitions.models import Competition
from teams.models import Team


class HomeView(TemplateView):
    '''
    This view is used to display the home page
    '''
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['user_team'] = Team.objects.filter(owner=self.request.user.id)
        context['user_competition'] = Competition.objects.filter(owner=self.request.user.id)
        return context
