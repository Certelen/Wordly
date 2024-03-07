from django.shortcuts import redirect, render
from players.models import Player
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.http import JsonResponse
import datetime

from .models import Lobby
from .serializers import LobbySerializer


def user_lobby_exist_and_get(player=False, lobby=False):
    if player:
        player = Player.objects.filter(username=player)
        if player:
            player = player[0]
    if lobby:
        lobby = Lobby.objects.filter(lobby_id=lobby)
        if lobby:
            lobby = lobby[0]
    return [player, lobby]


class LobbyViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer

    def create(self, request, *args, **kwargs):
        """Создание, либо поиск лобби."""
        player = user_lobby_exist_and_get(kwargs['username'], False)[0]
        if not player:
            raise ValidationError(
                'Игрока не существует'
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lobby = request.data['find_lobby']
        if lobby:
            """Поиск лобби."""
            now_lobby = user_lobby_exist_and_get(False, lobby)[1]
            if (not Lobby.objects.get(lobby_id=lobby).lobby_player):
                if player == now_lobby.lobby_creater:
                    return redirect(
                        f'../{kwargs["username"]}/{lobby}/',
                        permanent=True
                    )
                now_lobby.lobby_player = player
                now_lobby.save()
                player.lobby_id = lobby
                player.save()
                return redirect(
                    f'../{kwargs["username"]}/{lobby}/',
                    permanent=True
                )
            else:
                if player == now_lobby.lobby_player:
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
        data['created_date'] = datetime.datetime.now()
        data['win_word'] = Lobby.get_random_word(
            serializer.validated_data.get('create_lobby'))
        data['lobby_creater'].lobby_id = data['lobby_id']
        data['lobby_creater'].save()
        return serializer.save(
            **data
        )


@api_view(['GET', 'POST'])
def lobby_game(request, username, lobby_id, logic=False):
    """Обработчик игры со стороны сервера."""
    player, lobby = user_lobby_exist_and_get(username, lobby_id)
    if not (lobby and player):
        return redirect(
            '../../../login/',
            permanent=True
        )
    if (lobby.lobby_creater != player and
            lobby.lobby_player != player):
        return redirect(
            '../../../login/',
            permanent=True
        )
    if lobby.lobby_creater == player:
        now_player = 0
    else:
        now_player = 1
    template = 'wordly.html'
    winner = lobby.winner
    winword = None
    letters = len(lobby.win_word)

    if lobby.end_date:
        if lobby.winner:
            if lobby.winner == lobby.lobby_creater:
                winner = '1'
            else:
                winner = '2'
        else:
            winner = '0'
        winword = lobby.win_word

    if request.method == 'GET' and logic:
        return JsonResponse({
            'p0_words': lobby.used_words_player_one,
            'p1_words': lobby.used_words_player_two,
            'winner': winner,
            'winword': winword
        })

    if request.method == 'GET':
        return render(
            request, template,
            context={
                'now_player': now_player,
                'letters': letters,
                'p0_words': lobby.used_words_player_one,
                'p1_words': lobby.used_words_player_two,
                'winner': winner,
                'winword': winword
            },
        )

    if request.method == 'POST':
        guess_word = request.data['guess_word']
        guess_word = list(guess_word)
        post = False
        for letter_num in range(0, letters):
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
        if now_player == 0:
            if not (len(lobby.used_words_player_one) ==
                    len(lobby.used_words_player_two)):
                lobby.used_words_player_one += ''.join(guess_word)
                lobby.lobby_creater.attempts_guess += 1
                post = True
        else:
            if not (len(lobby.used_words_player_two) >
                    len(lobby.used_words_player_one)):
                lobby.used_words_player_two += ''.join(guess_word)
                lobby.lobby_player.attempts_guess += 1
                post = True
        if (request.data['guess_word'] == lobby.win_word or
                (len(lobby.used_words_player_one) == (4 *
                                                      letters * 5) and
                 len(lobby.used_words_player_two) == (4 *
                                                      letters * 5))):
            end_date = datetime.datetime.now()
            start_date = lobby.created_date.replace(tzinfo=None)
            duration_game = end_date - start_date
            lobby.end_date = end_date
            lobby.lobby_player.games += 1
            lobby.lobby_creater.games += 1
            lobby.lobby_creater.time_game += duration_game
            lobby.lobby_player.time_game += duration_game
            lobby.lobby_creater.lobby_id = ""
            lobby.lobby_player.lobby_id = ""
            winword = lobby.win_word
            winner = '0'
            if request.data['guess_word'] == lobby.win_word:
                lobby.winner = player
                if lobby.winner == lobby.lobby_creater:
                    winner = '1'
                else:
                    winner = '2'
                if lobby.lobby_creater == player:
                    lobby.lobby_creater.win_games += 1
                else:
                    lobby.lobby_player.win_games += 1
        Player.update_player(lobby.lobby_creater)
        Player.update_player(lobby.lobby_player)
        lobby.save()
        return JsonResponse({
            'p0_words': lobby.used_words_player_one,
            'p1_words': lobby.used_words_player_two,
            'winner': winner,
            'post': post,
            'winword': winword
        })
