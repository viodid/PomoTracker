from django.urls import path

from . import views

urlpatterns = [
    path('<str:token>', views.getAll, name='all'),
    path('<str:token>', views.create, name='create')
    #path('<str:token>/<int:pomodoro>', views.updateDelete, name='update-delete'),
    #path('<str:token>/leaderboard/<str:period>', views.updateDelete, name='leaderboard')
]
