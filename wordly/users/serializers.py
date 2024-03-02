from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = (
            'username',
        )

    def validate_username(self, username: str) -> None:
        if not username:
            raise serializers.ValidationError(
                'Заполните поле'
            )

        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" как имя.'
            )
        if Player.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с этим именем уже существует.'
            )
