from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import secrets

from .models import *


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        pomodoros = SlicePomodoros(user.pomodoros)
        token = generateToken(request)
        return render(request, 'app/index.html', {
            'pomodoros': pomodoros,
            'token': token
        })
    return render(request, 'app/index.html')


def privacy(request):
    return render(request, 'app/privacy.html')


def terms(request):
    return render(request, 'app/terms.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def apiReference(request):
    return render(request, 'app/api.html')


def token(request):

    if request.user.is_authenticated:
        token = generateToken(request)
        return render(request, 'app/token.html', {
            'message': token
        })

    return render(request, 'app/token.html', {
        'message': 'You need to be logged in.'
    })


def generateToken(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        token = secrets.token_urlsafe(20)
        if not Token.objects.filter(user=user):
            print('here')
            Token(user=user, token=token).save()
        return user.token.all()[0].token
    return None

