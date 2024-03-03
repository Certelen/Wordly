from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LobbyViewSet

router_v1 = SimpleRouter()
router_v1.register('', LobbyViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
