from django.contrib import admin
from .models import Pomodoro, UserSettings, Tag, Rewards

# Register your models here.
admin.site.register(Pomodoro)
admin.site.register(UserSettings)
admin.site.register(Tag)
admin.site.register(Rewards)
