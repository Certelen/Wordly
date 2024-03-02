from django.urls import path, include
from .views import index

urlpatterns = [
    path('users/', include('users.urls', namespace='users')),
    path('', index),
]
