from django.contrib import admin

from .models import Lobby


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    exclude = ('used_words_player_one', 'used_words_player_two',)
