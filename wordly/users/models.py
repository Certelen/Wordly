from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):
    lobbyId = models.CharField(
        'Id лобби',
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username
