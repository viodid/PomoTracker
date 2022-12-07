from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from datetime import datetime


class Pomodoro(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='pomodoros')
    datetime = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT, related_name='pomodoros')

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'created_at': self.datetime,
            'tag': self.tag.tag
        }

    def checkLastCreated(self):
        # Get user
        user = self.user
        # Check whether there is more than one Pomodoro
        if user.pomodoros.last() == user.pomodoros.first():
            return True
        date1 = self.datetime
        # Compare the last and before last pomodoros time stamps
        date2 = user.pomodoros.all().order_by('-id')[1].datetime
        diff = date1 - date2

        if (diff.total_seconds() / 60) < 24.9:
            return False

        return True

    def __str__(self):
        return f'{self.id}, {self.user}, {self.datetime}, {self.tag}'


class SlicePomodoros:

    def __init__(self, pomodoros, user):
        self.user = user
        self.all = pomodoros.all()
        self.year = pomodoros.filter(datetime__year=datetime.now().year)
        self.month = pomodoros.filter(datetime__month=datetime.now().month, datetime__year=datetime.now().year)
        self.week = pomodoros.filter(datetime__week=datetime.now().isocalendar().week, datetime__month=datetime.now().month, datetime__year=datetime.now().year)
        self.day = pomodoros.filter(datetime__day=datetime.now().day, datetime__week=datetime.now().isocalendar().week, datetime__month=datetime.now().month, datetime__year=datetime.now().year).order_by('datetime')


class Tag(models.Model):
    tag = models.CharField(max_length=24, null=False, unique=True)

    def __str__(self):
        return f'{self.tag}'


class Token(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=27, null=True)

    def __str__(self):
        return f'{self.token} from {self.user.username}'


class UserSettings(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='settings')
    white_theme = models.BooleanField(default=False)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    sound_choices_start = (
        ('DI', 'ding'),
        ('NA', 'nanana')
    )
    startSound = models.CharField(max_length=2, choices=sound_choices_start, default='DI')
    sound_choices_stop = (
        ('MI', 'minion'),
        ('WH', 'whoose')
    )
    stopSound = models.CharField(max_length=2, choices=sound_choices_stop, default='WH')
    focusTime = models.PositiveSmallIntegerField(default=25)
    breakTime = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f'{self.user.username}, {self.white_theme}, {self.image}'

    def serialize(self):
        return {
            'user': self.user.username,
            'white_theme': self.white_theme,
            'startSound': self.startSound,
            'stopSound': self.stopSound,
            'focusTime': self.focusTime,
            'breakTime': self.breakTime
        }


class Rewards(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='rewards')
    gold = models.PositiveSmallIntegerField(default=0)
    silver = models.PositiveSmallIntegerField(default=0)
    bronze = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}, {self.gold}, {self.silver}, {self.bronze}'
