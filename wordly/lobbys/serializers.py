from rest_framework import serializers

from .models import Lobby


class LobbySerializer(serializers.ModelSerializer):
    create_lobby = serializers.ChoiceField(
        {4, 5, 6},
        label='Создать лобби c выбранной длиной слова'
    )
    find_lobby = serializers.CharField(label='Найти лобби')

    class Meta:
        model = Lobby
        fields = (
            'find_lobby',
            'create_lobby',
            'lobby_creater',
            'win_word',
        )
        read_only_fields = (
            'lobby_creater',
            'win_word',
        )

    def validate(self, data):
        validate_find = data.get('find_lobby')
        validate_create = data.get('create_lobby')
        if not (validate_find or validate_create):
            raise serializers.ValidationError(
                'Выберите одно из действий'
            )
        if validate_find and Lobby.objects.filter(lobby_id=validate_find):
            raise serializers.ValidationError(
                'Лобби с таким Id не существует'
            )
        return data
