from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Pomodoro(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='pomodoros')
    datetime = models.DateTimeField(auto_now=True)
    tag = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.user}, {self.datetime}, {self.tag}'
