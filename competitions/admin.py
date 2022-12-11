from django.contrib import admin
#
# Register your models here.
from .models import Competition, Match, PlayerInTeam

admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(PlayerInTeam)
