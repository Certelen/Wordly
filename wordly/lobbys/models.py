from django.db import models

from users.models import Player


class Lobby(models.Model):
    lobby_creater = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='creater',
        verbose_name='Создатель лобби',
    )
    lobby_player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name='player',
        verbose_name='Второй игрок',
    )
    start = models.BooleanField(
        'Игра начата'
    )
    win_word = models.CharField(
        'Загаданное слово',
        max_length=6
    )

    def __str__(self):
        return 'Лобби игрока ' + self.lobby_creater
