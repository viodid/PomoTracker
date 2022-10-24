from django.urls import path

from . import views

urlpatterns = [
    path('<str:token>/get', views.getAll, name='all'),
    path('<str:token>/create', views.create, name='create'),
    path('<str:token>/<int:pomodoro_id>', views.updateDelete, name='update-delete'),
    path('<str:token>/settings', views.userSettings, name='user-settings')
]
