from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('effect', views.audio_effect, name='effect')
]
