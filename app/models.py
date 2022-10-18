from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


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

        if Pomodoro.objects.last() == Pomodoro.objects.first():
            return True
        date1 = self.datetime
        date2 = Pomodoro.objects.get(id=(self.id - 1)).datetime
        diff = date1 - date2
        print(date2, date1, diff)
        if (diff.total_seconds() / 60) < 24.9:
            return False

        return True

    def __str__(self):
        return f'{self.user}, {self.datetime}, {self.tag}'


class Tag(models.Model):
    tag = models.CharField(max_length=24, null=False)

    def __str__(self):
        return f'{self.tag}'


class UserToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=27, null=True)

    def __str__(self):
        return f'{self.token}'


