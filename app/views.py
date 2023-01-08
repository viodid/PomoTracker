from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
import secrets

from .models import User, SlicePomodoros, UserSettings, Rewards, Pomodoro
from .forms import ProfileForm


def index(request):
    if request.user.is_authenticated:
        generateUserSettings(request)
        # temporary
        checkMissingSettings(request)
        generateRewards(request)
        user = User.objects.get(username=request.user.username)
        pomodoros = SlicePomodoros(user.pomodoros, user)
        return render(request, 'app/index.html', {
                          'User': user,
                          'pomodoros': pomodoros
                      })
    return render(request, 'app/index.html')


def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == 'POST' and username == request.user.username:
            form = ProfileForm(request.POST, request.FILES, initial={
                                   'shortBreak': user.settings.shortBreak,
                                   'longBreak': user.settings.longBreak,
                                   #'focusColor': user.settings.focusColor,
                                   'startSound': user.settings.startSound,
                                   'stopSound': user.settings.stopSound
                               })

            if form.is_valid():
                saveSettings(form.cleaned_data, user)
                return render(request, 'app/profile.html', {
                                  'message': 'Profile updated successfully.',
                                  'form': form,
                                  'display': True,
                                  'userProfile': user,
                                  'averagePomos': Pomodoro.getAveragePomodoros(user)
                              })
            else:
                return render(request, 'app/profile.html', {
                                  'message': 'Invalid form',
                                  'message_class': 'error'
                              })

        if request.user.username == username:
            form = ProfileForm(initial={
                                   'shortBreak': user.settings.shortBreak,
                                   'longBreak': user.settings.longBreak,
                                   #'focusColor': user.settings.focusColor,
                                   'startSound': user.settings.startSound,
                                   'stopSound': user.settings.stopSound
                               })
            return render(request, 'app/profile.html', {
                              'form': form,
                              'display': True,
                              'userProfile': user,
                              'averagePomos': Pomodoro.getAveragePomodoros(user)
                          })

    if User.objects.filter(username=username):
        userProfile = User.objects.get(username=username)
        return render(request, 'app/profile.html', {
                          'userProfile': userProfile,
                          'averagePomos': Pomodoro.getAveragePomodoros(userProfile)
                      })
    return HttpResponseNotFound(request)


def saveSettings(form, user):
    print(form)
    settings = user.settings
    if form['image']:
        settings.name = form['image']
    if form['shortBreak']:
        settings.shortBreak = int(form['shortBreak'])
    if form['longBreak']:
        settings.longBreak = int(form['longBreak'])
    #if form['focusColor']:
        #settings.focusColor = form['focusColor']
    if form['startSound']:
        settings.startSound = form['startSound']
    if form['stopSound']:
        settings.stopSound = form['stopSound']
    settings.save()


@login_required
def pomodorosList(request):
    user = User.objects.get(username=request.user.username)
    pomodoros = user.pomodoros.all().order_by('-datetime')
    paginator = Paginator(pomodoros, 50)

    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    return render(request, 'app/pomodoros.html', {
                      'page_obj': pageObj
                  })


@login_required
def charts(request):
    user = User.objects.get(username=request.user.username)
    #pomodoros = user.pomodoros.filter()
    return render(request, 'app/charts.html')


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
                          'message': 'Invalid period url',
                          'message_class': 'error'
                      })


def generateToken(request):
    user = User.objects.get(username=request.user.username)
    token = secrets.token_urlsafe(16)
    if not user.settings.token:
        user.settings.token = token
        user.settings.save()


def generateColors(request):
    user = User.objects.get(username=request.user.username)
    if not user.settings.breakColor:
        user.settings.color = '#ADFF2F'
    if not user.settings.focusColor:
        user.settings.focusColor = '#F1C232'
    user.settings.save()


def generateSoundsAndTime(request):
    user = User.objects.get(username=request.user.username)
    if not user.settings.startSound:
        user.settings.startSound = '#ding'
    if not user.settings.stopSound:
        user.settings.stopSound = '#whoosh'
    if not user.settings.longBreak:
        user.settings.longBreak = 15
    user.settings.save()


def checkMissingSettings(request):
    if request.user.is_authenticated:
        generateToken(request)
        generateColors(request)
        generateSoundsAndTime(request)
    return None


def generateUserSettings(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if not UserSettings.objects.filter(user=user):
            UserSettings(user=user).save()
        return user.settings
    return None

def generateRewards(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if not Rewards.objects.filter(user=user):
            Rewards(user=user).save()
        return user.rewards
    return None
