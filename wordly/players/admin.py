from django.contrib import admin

from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    exclude = ('now_game_date', 'games', 'attempts_guess', 'time_game',)
