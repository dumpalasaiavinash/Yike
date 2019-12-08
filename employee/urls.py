# from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'employee'

urlpatterns = [
    path('<int:j>', views.dashboard, name='dashboard'),
    path('juniors/', views.juniors, name='juniors'),
    path('validate/<str:complaint_id>/<int:org_id>',views.validate, name='validate')
]
