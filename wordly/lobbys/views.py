from rest_framework import mixins, viewsets, status, response
from rest_framework.decorators import action
from django.shortcuts import redirect

from .serializers import LobbySerializer
from .models import Lobby


class LobbyViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.data['find_lobby']:


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    @action(
        methods=['POST'],
        detail=False,
    )
    def find_lobby(self, request):
        serialized = LobbySerializer(data=request.data)
        return response.Response(
            'No',
            status=status.HTTP_400_BAD_REQUEST
        )
