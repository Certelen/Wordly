from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


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

    def __str__(self):
        return self.username
