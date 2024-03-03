from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lobby/', include('lobbys.urls')),
    path('', include('players.urls')),
]
