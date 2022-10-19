from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import secrets

from .models import *


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        pomodoros = SlicePomodoros(user.pomodoros)
        return render(request, 'app/index.html', {
            'pomodoros': pomodoros
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


def generateToken(request):

    if request.user.is_authenticated:

        token = secrets.token_urlsafe(20)
        user = User.objects.get(username=request.user.username)
        UserToken(user=user, token=token).save()

        return render(request, 'app/token.html', {
            'message': token
        })

    return render(request, 'app/token.html', {
        'message': 'You need to be logged in.'
    })
