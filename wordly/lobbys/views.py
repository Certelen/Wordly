from django.shortcuts import redirect, render
from players.models import Player
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError

from .models import Lobby
from .serializers import LobbySerializer


class LobbyViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer

    def create(self, request, *args, **kwargs):
        """Создание, либо поиск лобби."""
        player = Player.objects.filter(username=kwargs['username'])
        if not player:
            raise ValidationError(
                'Игрока не существует'
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = request.data['find_lobby']
        if lobby:
            """Поиск лобби."""
            now_lobby = Lobby.objects.get(lobby_id=lobby)
            if (not Lobby.objects.get(lobby_id=lobby).lobby_player):
                if player[0] == now_lobby.lobby_creater:
                    return redirect(
                        f'../{kwargs["username"]}/{lobby}/',
                        permanent=True
                    )
                now_lobby.lobby_player = player[0]
                now_lobby.save()
                player[0].lobby_id = lobby
                player[0].save()
                return redirect(
                    f'../{kwargs["username"]}/{lobby}/',
                    permanent=True
                )
            else:
                if player[0] == now_lobby.lobby_player:
                    return redirect(
                        f'../{kwargs["username"]}/{lobby}/',
                        permanent=True
                    )
                raise ValidationError(
                    'В лобби уже есть второй игрок!'
                )
        self.perform_create(serializer, **kwargs)
        return redirect(
            f'{Player.objects.get(username=kwargs["username"]).lobby_id}/',
            permanent=True
        )

    def perform_create(self, serializer, data={}, **kwargs):
        """Создание лобби."""
        data['lobby_creater'] = Player.objects.get(
            username=kwargs['username'])
        if data['lobby_creater'].lobby_id:
            raise ValidationError(
                'Вы уже учавствуете в игре, id игры: ' +
                data['lobby_creater'].lobby_id
            )
        data['lobby_id'] = Lobby.create_lobby_id()
        data['win_word'] = Lobby.get_random_word(
            serializer.validated_data.get('create_lobby'))
        data['lobby_creater'].lobby_id = data['lobby_id']
        data['lobby_creater'].save()
        return serializer.save(
            **data
        )


@api_view(['GET', 'POST'])
def lobby_game(request, username, lobby_id):
    """Обработчик игры со стороны сервера."""
    if not (Player.objects.filter(username=username) and
            Lobby.objects.filter(lobby_id=lobby_id)):
        return redirect(
            '../../../login/',
            permanent=True
        )
    template = 'wordly.html'
    lobby = Lobby.objects.get(lobby_id=lobby_id)
    player = Player.objects.get(username=username)
    if lobby.lobby_creater == player:
        now_player = '0'
    else:
        now_player = '1'
    if lobby.winner:
        if lobby.lobby_creater == lobby.winner:
            winner = "1"
        else:
            winner = "2"
    else:
        winner = "0"
    if request.method == 'POST':
        guess_word = request.data['guess_word']
        if guess_word == lobby.win_word:
            lobby.winner = player
            lobby.lobby_creater.lobby_id = ""
            lobby.lobby_player.lobby_id = ""
            lobby.lobby_creater.save()
            lobby.lobby_player.save()
        guess_word = list(guess_word)
        for letter_num in range(0, len(lobby.win_word)):
            if guess_word[letter_num] == lobby.win_word[letter_num]:
                guess_word[letter_num] += ':2'
            elif guess_word[letter_num] in lobby.win_word:
                guess_word[letter_num] += ':1'
            else:
                guess_word[letter_num] += ':0'
            if letter_num == len(guess_word)-1:
                guess_word += ";"
            else:
                guess_word[letter_num] += ","
        if lobby.lobby_creater == player:
            lobby.used_words_player_one += ''.join(guess_word)
        elif lobby.lobby_player == player:
            lobby.used_words_player_two += ''.join(guess_word)
        lobby.save()

    return render(
        request, template,
        context={
            'now_player': now_player,
            'p1_words': lobby.used_words_player_one[:-1],
            'p2_words': lobby.used_words_player_two[:-1],
            'letters': len(lobby.win_word),
            'winner': winner
        },
    )
