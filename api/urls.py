from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/get/<str:endpoint>', views.getAll),
    path('<str:token>/getSettings', views.getSettings),
    path('<str:token>/create', views.create, name='create'),
    path('<str:token>/<int:pomodoro_id>', views.updateDelete),
    path('<str:token>/settings', views.updateSettings)
]
