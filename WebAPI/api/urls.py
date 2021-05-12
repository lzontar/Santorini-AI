from django.urls import path

from . import views

urlpatterns = [
    path('move', views.move, name='move'),
    path('init', views.init, name='init'),
    path('choose', views.choose, name='choose'),
    path('build', views.build, name='build')
]
