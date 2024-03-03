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
            return redirect('../lobby/', permanent=True)
        if serialized.is_valid():
            player = Player.objects.create(username=request.data['username'])
            return redirect('../lobby/', permanent=True)
        else:
            return response.Response(
                serialized._errors,
                status=status.HTTP_400_BAD_REQUEST
            )
