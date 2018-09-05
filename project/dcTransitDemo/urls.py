from django.conf.urls import url
from django.urls import path
from django.conf.urls import re_path, include
from . import views

urlpatterns = [
    url(r'^$', views.handleRequest, name='handleRequest'),
    url(r'^metrobusstops/', views.handleMetrobusStops, name='handleMetrobusStops'),
    url(r'^circulatorroutes/', views.handleCirculatorRoutes, name='handleCirculatorRoutes'),
    url(r'^circulatorstops/', views.handleCirculatorStops, name='handleCirculatorStops')
]
