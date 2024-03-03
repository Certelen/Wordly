from rest_framework import mixins, viewsets, status, response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view

from django.shortcuts import redirect, render

from .serializers import LobbySerializer
from .models import Lobby
from players.models import Player


class LobbyViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer

    def create(self, request, *args, **kwargs):
        player = Player.objects.filter(username=kwargs['username'])
        if not player:
            raise ValidationError(
                'Игрока не существует'
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = request.data['find_lobby']
        if lobby and not Lobby.objects.get(lobby_id=lobby).lobby_player:
            player[0].lobby_id = lobby
            player[0].save()
            return redirect(
                f'../lobby/{request.username}/{lobby}/',
                permanent=True
            )
        self.perform_create(serializer, **kwargs)
        return redirect(
            f'{Player.objects.get(username=kwargs["username"]).lobby_id}/',
            permanent=True
        )

    def perform_create(self, serializer, data={}, **kwargs):
        data['lobby_creater'] = Player.objects.get(
            username=kwargs['username'])
        if data['lobby_creater'].lobby_id:
            raise ValidationError(
                'Вы уже учавствуете в игре'
            )
        data['lobby_id'] = Lobby.create_lobby_id()
        data['win_word'] = Lobby.get_random_word(
            serializer.validated_data.get('create_lobby'))
        data['lobby_creater'].lobby_id = data['lobby_id']
        data['lobby_creater'].save()
        return serializer.save(
            **data
        )


@api_view(['GET'])
def lobby_game(request, username, lobby_id):
    if not (Player.objects.filter(username=username) and
            Lobby.objects.filter(lobby_id=lobby_id)):
        return redirect(
            '../../../login/',
            permanent=True
        )
    if request.method == 'GET':
        template = 'wordly.html'
        return render(request, template, context={'SIGNUP': True})
