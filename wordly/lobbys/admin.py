from django.contrib import admin

from .models import Lobby


@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    pass
