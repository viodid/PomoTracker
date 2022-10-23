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
        user_settings = UserSettings.objects.get(user=user)
        return render(request, 'app/index.html', {
            'pomodoros': pomodoros,
            'token': token,
            'settings': user_settings
        })
    return render(request, 'app/index.html')


def privacy(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_settings = UserSettings.objects.get(user=user)
        return render(request, 'app/privacy.html', {
            'settings': user_settings
        })
    return render(request, 'app/privacy.html')


def terms(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_settings = UserSettings.objects.get(user=user)
        return render(request, 'app/terms.html', {
            'settings': user_settings
        })
    return render(request, 'app/terms.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def apiReference(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        user_settings = UserSettings.objects.get(user=user)
        return render(request, 'app/api.html', {
            'settings': user_settings
        })
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


def leaderboard(request, period):

    slice_pomodoro_users = []
    for user in User.objects.all():
        pomodoros = SlicePomodoros(user.pomodoros)
        slice_pomodoro_users.append(pomodoros)

    if request.user.is_authenticated:

        user = User.objects.get(username=request.user.username)
        user_settings = UserSettings.objects.get(user=user)

        if period == 'day':
            day = sorted(slice_pomodoro_users, key=lambda pomos: pomos.day.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.day for pomo in day],
                'settings': user_settings
            })
        elif period == 'week':
            week = sorted(slice_pomodoro_users, key=lambda pomos: pomos.week.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.week for pomo in week],
                'settings': user_settings
            })
        elif period == 'month':
            month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.month for pomo in month],
                'settings': user_settings
            })
        elif period == 'year':
            year = sorted(slice_pomodoro_users, key=lambda pomos: pomos.year.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.year for pomo in year],
                'settings': user_settings
            })
        elif period == 'all':
            all = sorted(slice_pomodoro_users, key=lambda pomos: pomos.all.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.all for pomo in all],
                'settings': user_settings
            })
        else:
            return render(request, 'app/leaderboard.html', {
                'message': 'Invalid period url',
                'settings': user_settings
            })

    else:
        month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)
        return render(request, 'app/leaderboard.html', {
            'pomos': [pomo.month for pomo in month]
        })

