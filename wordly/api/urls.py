from django.urls import path, include

urlpatterns = [
    path('lobby/', include('lobbys.urls')),
    path('', include('players.urls'))
]
