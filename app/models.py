from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from datetime import datetime
from math import ceil


class Pomodoro(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='pomodoros')
    datetime = models.DateTimeField(default=timezone.now)
    tag = models.ForeignKey('Tag', on_delete=models.PROTECT,
                            related_name='pomodoros')

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
        self.month = pomodoros.filter(datetime__month=datetime.now().month,
                                      datetime__year=datetime.now().year)
        self.week = pomodoros.filter(datetime__week=datetime.now()
                                     .isocalendar().week,
                                     datetime__month=datetime.now().month,
                                     datetime__year=datetime.now().year)
        self.day = pomodoros.filter(datetime__day=datetime.now().day,
                                    datetime__week=datetime.now()
                                    .isocalendar().week,
                                    datetime__month=datetime.now().month,
                                    datetime__year=datetime
                                    .now().year).order_by('datetime')


class Tag(models.Model):
    tag = models.CharField(max_length=24, null=False, unique=True)

    def __str__(self):
        return f'{self.tag}'


class UserSettings(models.Model):
    sound_choices_start = (
        ('#ding', 'ding'),
        ('#folks', 'nanana')
    )
    sound_choices_stop = (
        ('#minion', 'minion'),
        ('#whoosh', 'whoosh')
    )
    theme_choices = (
        ('default', 'default'),
        ('white', 'white'),
        ('forest', 'forest'),
        ('aquamarine', 'aquamarine'),
        ('garnet', 'garnet'),
        ('coral', 'coral'),
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                related_name='settings')
    token = models.CharField(max_length=27, null=True, unique=True)
    theme = models.CharField(max_length=16, default='default', choices=theme_choices)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    startSound = models.CharField(max_length=16,
                                  choices=sound_choices_start, default='#ding')
    stopSound = models.CharField(max_length=16, choices=sound_choices_stop,
                                 default='#whoosh')
    focusTime = models.PositiveSmallIntegerField(default=25)
    shortBreak = models.PositiveSmallIntegerField(default=5)
    longBreak = models.PositiveSmallIntegerField(default=15)
    focusColor = models.CharField(default='#f1c232', max_length=7)
    breakColor = models.CharField(default='#ADFF2F', max_length=7)
    timezone = models.CharField(max_length=64, default='UTC')

    def serialize(self):
        return {
            'user': self.user.username,
            'theme': self.theme,
            'startSound': self.startSound,
            'stopSound': self.stopSound,
            'focusTime': self.focusTime,
            'longBreak': self.longBreak,
            'shortBreak': self.shortBreak,
            'focusColor': self.focusColor,
            'breakColor': self.breakColor,
            'token': self.token
        }

    def __str__(self):
        return f'''{self.user.username}, {self.theme}, {self.image},
        {self.startSound}, {self.stopSound}, {self.focusTime}, {self.longBreak},
        {self.shortBreak}, {self.focusColor}, {self.breakColor}, {self.token,
        {self.timezone}}'''


class Rewards(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                related_name='rewards')
    gold = models.PositiveSmallIntegerField(default=0)
    silver = models.PositiveSmallIntegerField(default=0)
    bronze = models.PositiveSmallIntegerField(default=0)
    ranks = ArrayField(ArrayField(models.IntegerField()), default=list)

    def getAverageRank(self):
        if len(self.ranks) <= 1:
            return 'No rank'
        average = 0
        for i, rank in enumerate(self.ranks):
            if i != 0:
                average += self.ranks[i]
        return ceil(average / (len(self.ranks) - 1))

    def __str__(self):
        return f'''{self.user.username}, {self.gold},
        {self.silver}, {self.bronze}, {self.ranks}'''


class Statistics(models.Model):

    @staticmethod
    def getAveragePomodoros(user):
        # Get all pomodoros
        pomodoros = user.pomodoros.all()
        # Make sure there are pomodoros
        if not pomodoros:
            return 0
        # Get the first pomodoro
        first = pomodoros.first()
        # Get the difference between the first pomodoro day and today
        diff = timezone.now() - first.datetime
        # Get the number of pomodoros
        num = pomodoros.count()
        # Get the average pomodoros per day
        try:
            avg = num / diff.days
        except ZeroDivisionError:
            avg = num
        return round(avg, ndigits=2)

    @staticmethod
    def aggregatePomodorosByTag(user):
        # Get all pomodoros
        pomodoros = user.pomodoros.all()
        # Make sure there are pomodoros
        if not pomodoros:
            return {}
        # Get all tags
        tags = Tag.objects.all()
        # Initialize the dictionary
        tagDict = {}
        # Loop through all tags
        for tag in tags:
            # Get all pomodoros with the tag
            pomodorosWithTag = pomodoros.filter(tag=tag)
            # Get the number of pomodoros with the tag
            num = pomodorosWithTag.count()
            # Add the number of pomodoros with the tag to the dictionary if it
            #  not 0
            if num != 0:
                tagDict[tag.tag] = num
        return dict(sorted(tagDict.items(), key=lambda x: x[1], reverse=True))
