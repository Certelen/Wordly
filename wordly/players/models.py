from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from datetime import timedelta


class Player(models.Model):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "Никнейм",
        max_length=150,
        unique=True,
        help_text=(
            "Обязательно. 150 символов или меньше. "
            "Только буквы, цифры и @/./+/-/_ ."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь с таким ником уже существует",
        },
    )
    lobby_id = models.CharField(
        'Id лобби',
        max_length=20,
        null=True,
        blank=True
    )
    games = models.IntegerField(
        'Количество игр',
        default=0
    )
    win_games = models.IntegerField(
        'Количество выйгранных игр',
        default=0
    )
    win_games_percen = models.IntegerField(
        'Процент побед',
        default=0
    )
    time_game = models.DurationField(
        'Общее время игры',
        default=timedelta
    )
    average_time = models.DurationField(
        'Среднее время игры',
        default=timedelta
    )
    attempts_guess = models.IntegerField(
        'Количество попыток угадать слово',
        default=0
    )
    average_attempts_guess = models.FloatField(
        'Среднее количество попыток угадать слово',
        default=0
    )

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ('created_date',)

    @staticmethod
    def update_player(player):
        if player.games:
            player.win_games_percen = int(
                player.win_games / player.games * 100)
            player.average_time = player.time_game / player.games
            player.average_attempts_guess = "{:.2f}".format(
                player.attempts_guess / player.games)
        player.save()

    def __str__(self):
        return self.username
