# from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('juniors/', views.juniors, name='juniors')
]
