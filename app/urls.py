from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms')
]