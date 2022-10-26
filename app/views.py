from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
import secrets

from .models import *


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        pomodoros = SlicePomodoros(user.pomodoros, user)
        generateToken(request)
        generateUserSettings(request)
        generateRewards(request)
        return render(request, 'app/index.html', {
            'pomodoros': pomodoros
        })
    return render(request, 'app/index.html')


def profile(request, username):
    if User.objects.filter(username=username):
        user = User.objects.get(username=username)
        return render(request, 'app/profile.html', {
            'user': user
        })
    return HttpResponseNotFound(request)


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
            Token(user=user, token=token).save()
        return user.token.token
    return None


def generateUserSettings(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if not UserSettings.objects.filter(user=user):
            UserSettings(user=user, white_theme=False).save()
        return user.settings
    return None


def leaderboard(request, period):

    slice_pomodoro_users = []
    for user in User.objects.all():
        pomodoros = SlicePomodoros(user.pomodoros, user)
        slice_pomodoro_users.append(pomodoros)

    if request.user.is_authenticated:
        if period == 'day':
            day = sorted(slice_pomodoro_users, key=lambda pomos: pomos.day.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.day for pomo in day]
            })
        elif period == 'week':
            week = sorted(slice_pomodoro_users, key=lambda pomos: pomos.week.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.week for pomo in week]
            })
        elif period == 'month':
            month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.month for pomo in month]
            })
        elif period == 'year':
            year = sorted(slice_pomodoro_users, key=lambda pomos: pomos.year.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.year for pomo in year]
            })
        elif period == 'all':
            all = sorted(slice_pomodoro_users, key=lambda pomos: pomos.all.count(), reverse=True)
            return render(request, 'app/leaderboard.html', {
                'pomos': [pomo.all for pomo in all]
            })
        else:
            return render(request, 'app/leaderboard.html', {
                'message': 'Invalid period url'
            })

    else:
        month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)
        return render(request, 'app/leaderboard.html', {
            'pomos': [pomo.month for pomo in month]
        })


def generateRewards(request):
    if request.user.is_authenticated:
        if Rewards.objects.filter(user=request.user):
            return Rewards.objects.get(user=request.user)
        Rewards(user=request.user).save()
        return Rewards.objects.get(user=request.user)

