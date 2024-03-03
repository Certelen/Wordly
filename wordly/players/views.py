from rest_framework import mixins, viewsets, status, response
from rest_framework.decorators import action
from django.shortcuts import redirect

from .serializers import PlayerSerializer
from .models import Player


class PlayerViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(
        methods=['POST'],
        detail=False,
    )
    def login(self, request):
        serialized = PlayerSerializer(data=request.data)
        player = Player.objects.filter(username=request.data['username'])
        if player:
            lobby = player[0].lobby_id
            if lobby:
                return redirect(
                    f'../lobby/{player[0].username}/{lobby}/',
                    permanent=True
                )
            return redirect(
                f'../lobby/{player[0].username}/',
                permanent=True
            )
        if serialized.is_valid():
            player = Player.objects.create(username=request.data['username'])
            return redirect(
                f'../lobby/{player[0].username}/',
                permanent=True
            )
        else:
            return response.Response(
                serialized._errors,
                status=status.HTTP_400_BAD_REQUEST
            )
