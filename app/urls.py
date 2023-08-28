from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('api_reference', views.apiReference, name='api'),
    path('token', views.token, name='token'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('<str:username>/', views.profile, name='profile'),
    path('pomodoros', views.pomodorosList, name='pomodoros'),
    path('charts', views.charts, name='charts')
]
