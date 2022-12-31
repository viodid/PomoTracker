from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
import secrets
import PomoTracker

from .models import User, SlicePomodoros
from .forms import ProfileForm


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        pomodoros = SlicePomodoros(user.pomodoros, user)
        return render(request, 'app/index.html', {
                          'User': user,
                          'pomodoros': pomodoros
                          #'build': PomoTracker.__build__
                      })
    return render(request, 'app/index.html')


def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == 'POST' and username == request.user.username:
            form = ProfileForm(request.POST, request.FILES)

            if form.is_valid():
                cleanData = form.cleaned_data
                settings = user.settings
                settings.image = cleanData['image']
                settings.save()
                return render(request, 'app/profile.html', {
                                  'form': ProfileForm,
                                  'display': True,
                                  'message': 'Successfully uploaded'
                              })
            else:
                return render(request, 'app/profile.html', {
                                  'message': 'Invalid form'
                              })

        if request.user.username == username:
            return render(request, 'app/profile.html', {
                              'form': ProfileForm,
                              'display': True,
                              'userProfile': user
                          })

    if User.objects.filter(username=username):
        userProfile = User.objects.get(username=username)
        return render(request, 'app/profile.html', {
                          'userProfile': userProfile
                      })
    return HttpResponseNotFound(request)


def pomodorosList(request):
    user = User.objects.get(username=request.user.username)
    pomodoros = user.pomodoros.all().order_by('-datetime')
    return render(request, 'app/pomodoros.html', {
                      'pomodoros': pomodoros
                  })


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
        user = User.objects.get(username=request.user.username)
        if user.settings.token is None:
            user.settings.token = secrets.token_urlsafe(16)
            user.settings.save()
        return render(request, 'app/token.html', {
                          'message': user.settings.token
                      })
    return render(request, 'app/token.html', {
                      'message': 'You need to be logged in.'
                  })


def leaderboard(request, period):

    slice_pomodoro_users = []
    for user in User.objects.all():
        pomodoros = SlicePomodoros(user.pomodoros, user)
        slice_pomodoro_users.append(pomodoros)

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
