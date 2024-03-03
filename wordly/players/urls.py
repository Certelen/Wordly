from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PlayerViewSet

router_v1 = SimpleRouter()
router_v1.register('', PlayerViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
