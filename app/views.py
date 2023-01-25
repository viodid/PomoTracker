from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
import secrets

from .models import User, SlicePomodoros, UserSettings, Rewards, Statistics
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
            'pomodoros': pomodoros
        })
    return render(request, 'app/index.html')


def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if username == request.user.username:
            tags = tuple(Statistics.aggregatePomodorosByTag(user).items())
            paginator = Paginator(tags, 13)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            form = ProfileForm(initial={
                'shortBreak': user.settings.shortBreak,
                'longBreak': user.settings.longBreak,
                'theme': user.settings.theme,
                # 'focusColor': user.settings.focusColor,
                'startSound': user.settings.startSound,
                'stopSound': user.settings.stopSound,
                'timezone': user.settings.timezone,
            })
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, initial={
                    'shortBreak': user.settings.shortBreak,
                    'longBreak': user.settings.longBreak,
                    'theme': user.settings.theme,
                    # 'focusColor': user.settings.focusColor,
                    # 'startSound': user.settings.startSound,
                    'stopSound': user.settings.stopSound,
                    'timezone': user.settings.timezone,
                })
                if form.is_valid():
                    saveSettings(form.cleaned_data, user)
                    return render(request, 'app/profile.html', {
                        'message': 'Settings saved successfully',
                        'form': form,
                        'display': True,
                        'userProfile': user,
                        'averagePomos': Statistics.getAveragePomodoros(user),
                        'page_obj': page_obj,
                    })
                else:
                    return render(request, 'app/profile.html', {
                        'message': 'Invalid form',
                        'form': form,
                        'display': True,
                        'userProfile': user,
                        'averagePomos': Statistics.getAveragePomodoros(user),
                        'page_obj': page_obj,
                    })
            return render(request, 'app/profile.html', {
                'form': form,
                'display': True,
                'userProfile': user,
                'averagePomos': Statistics.getAveragePomodoros(user),
                'page_obj': page_obj
            })

    if User.objects.filter(username=username):
        userProfile = User.objects.get(username=username)
        return render(request, 'app/profile.html', {
            'userProfile': userProfile,
            'averagePomos': Statistics.getAveragePomodoros(userProfile)
        })
    return HttpResponseNotFound(request)


def saveSettings(form, user):
    settings = user.settings
    if form['image']:
        settings.image = form['image']
    if form['shortBreak']:
        settings.shortBreak = int(form['shortBreak'])
    if form['longBreak']:
        settings.longBreak = int(form['longBreak'])
    if form['theme']:
        settings.theme = form['theme']
        if form['theme'] == 'forest':
            settings.focusColor = '#EAE7B1'
        elif form['theme'] == 'aquamarine':
            settings.focusColor = '#6BAAAA'
        elif form['theme'] == 'default':
            settings.focusColor = '#f1c232'
        elif form['theme'] == 'garnet':
            settings.focusColor = '#9a1b18'
        elif form['theme'] == 'coral':
            settings.focusColor = '#FAD6A5'
    #if form['focusColor']:
    #settings.focusColor = form['focusColor']
    if form['startSound']:
        settings.startSound = form['startSound']
    if form['stopSound']:
        settings.stopSound = form['stopSound']
    if form['timezone']:
        settings.timezone = form['timezone']
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
        pomos = [pomo.day for pomo in day]
        paginator = Paginator(pomos, 50)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        return render(request, 'app/leaderboard.html', {
            'pomos': pageObj
        })
    elif period == 'week':
        week = sorted(slice_pomodoro_users, key=lambda pomos: pomos.week.count(), reverse=True)
        pomos = [pomo.week for pomo in week]
        paginator = Paginator(pomos, 50)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        return render(request, 'app/leaderboard.html', {
            'pomos': pageObj
        })
    elif period == 'month':
        month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)
        pomos = [pomo.month for pomo in month]
        paginator = Paginator(pomos, 50)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        return render(request, 'app/leaderboard.html', {
            'pomos': pageObj
        })
    elif period == 'year':
        year = sorted(slice_pomodoro_users, key=lambda pomos: pomos.year.count(), reverse=True)
        pomos = [pomo.year for pomo in year]
        paginator = Paginator(pomos, 50)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        return render(request, 'app/leaderboard.html', {
            'pomos': pageObj
        })
    elif period == 'all':
        all = sorted(slice_pomodoro_users, key=lambda pomos: pomos.all.count(), reverse=True)
        pomos = [pomo.all for pomo in all]
        paginator = Paginator(pomos, 50)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        return render(request, 'app/leaderboard.html', {
            'pomos': pageObj
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
