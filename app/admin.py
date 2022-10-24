from django.contrib import admin
from .models import Pomodoro, Token, UserSettings, Tag

# Register your models here.
admin.site.register(Pomodoro)
admin.site.register(Token)
admin.site.register(UserSettings)
admin.site.register(Tag)

