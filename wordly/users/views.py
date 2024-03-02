from rest_framework import status, response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse

from .serializers import PlayerSerializer
from .models import Player


@api_view(['POST'])
def login(request):
    serialized = PlayerSerializer(data=request.data)
    if serialized.is_valid():
        if Player.objects.filter(username=request.data['username']):
            return response.Response(
                JsonResponse({'username': request.data['username']}),
                status=status.HTTP_200_OK
            )
        template = 'users/signup.html'
        return render(request, template, context={'SIGNUP': True})
    else:
        return response.Response(
            JsonResponse({'username': None}),
            status=status.HTTP_200_OK
        )
