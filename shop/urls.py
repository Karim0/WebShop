from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'Shop'

urlpatterns = [
    path('', views.home_page, name='index'),
]