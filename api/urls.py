from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/alltags', views.getAllUserTags),
    path('<str:username>/alldates', views.getAllUserPomosDates),
    path('<str:username>/allpomodoros', views.getAllUserPomodoros),
    path('<str:token>/getSettings', views.getSettings),
    path('<str:token>/create', views.create, name='create'),
    path('<str:token>/<int:pomodoro_id>', views.updateDelete),
    path('<str:token>/updateTag/<str:tag_to_replace>', views.updateTags),
    path('<str:token>/settings', views.updateSettings)
]
