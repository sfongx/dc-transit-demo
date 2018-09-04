from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.handleRequest, name='handleRequest'),
    url(r'^metrobushelp/', views.handleMetrobusHelp, name='handleMetrobusHelp')
]
