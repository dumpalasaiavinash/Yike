from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('logged_in/', views.home_log, name='home_log'),
    path('registered/', views.home_reg, name='home_reg'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
