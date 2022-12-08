from django.contrib import admin
#
# Register your models here.
from .models import Player, Team, Competition, Match, PlayerInTeam

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(PlayerInTeam)

