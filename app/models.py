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
        # Check whether there is more than one Pomodoro
        if Pomodoro.objects.last() == Pomodoro.objects.first():
            return True
        date1 = self.datetime
        # Compare the last and before last pomodoros time stamps
        date2 = Pomodoro.objects.all().order_by('-id')[1].datetime
        diff = date1 - date2

        if (diff.total_seconds() / 60) < 24.9:
            return False

        return True

    def __str__(self):
        return f'{self.id}, {self.user}, {self.datetime}, {self.tag}'


class SlicePomodoros:

    def __init__(self, pomodoros, username):
        self.user = username
        self.day = pomodoros.filter(datetime__day=datetime.now().day).order_by('datetime')
        self.week = pomodoros.filter(datetime__week=datetime.now().isocalendar().week)
        self.month = pomodoros.filter(datetime__month=datetime.now().month)
        self.year = pomodoros.filter(datetime__year=datetime.now().year)
        self.all = pomodoros.all()


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
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}, {self.white_theme}, {self.image}'
