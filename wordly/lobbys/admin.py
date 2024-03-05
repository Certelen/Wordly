from django.contrib import admin

from .models import Lobby


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = ('lobby_id', 'lobby_creater',
                    'lobby_player', 'winner', 'winword')
