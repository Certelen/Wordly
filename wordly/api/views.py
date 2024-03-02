from django.shortcuts import render


def index(request):
    template = 'users/login.html'
    return render(request, template)
