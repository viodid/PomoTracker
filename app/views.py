"""Views for the app."""
import secrets
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .models import User, SlicePomodoros, UserSettings, Rewards, Statistics
from .forms import ProfileForm
from . import helpers



def index(request):
    """Display the index page"""
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
    """Display the profile page"""
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
                'startSound': user.settings.startSound,
                'stopSound': user.settings.stopSound,
                'timezone': user.settings.timezone,
            })
            if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES, initial={
                    'shortBreak': user.settings.shortBreak,
                    'longBreak': user.settings.longBreak,
                    'theme': user.settings.theme,
                    'startSound': user.settings.startSound,
                    'stopSound': user.settings.stopSound,
                    'timezone': user.settings.timezone,
                })
                if form.is_valid():
                    helpers.saveSettings(form.cleaned_data, user)
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


@login_required
def pomodorosList(request):
    """Display all pomodoros of the user"""
    user = User.objects.get(username=request.user.username)
    pomodoros = user.pomodoros.all().order_by('-datetime')
    paginator = Paginator(pomodoros, 50)

    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    return render(request, 'app/pomodoros.html', {
        'page_obj': pageObj
    })


#@cache_page(60 * 15)
def leaderboard(request):
    """Display the leaderboard page"""
    return render(request, 'app/leaderboard.html')


@login_required
@cache_page(60 * 3600)
def charts(request):
    """Display the charts page"""
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


def generateToken(request):
    """Generate a token for the user if he doesn't have one"""
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
