# from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),

]