from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LobbyViewSet, lobby_game

router_v1 = SimpleRouter(trailing_slash=True)
router_v1.register(r'(?P<username>.*)', LobbyViewSet)

urlpatterns = [
    path('<str:username>/<str:lobby_id>/<str:logic>',
         lobby_game),
    path('<str:username>/<str:lobby_id>/',
         lobby_game),
    path('', include(router_v1.urls)),
]
