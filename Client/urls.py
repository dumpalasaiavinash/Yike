from django.urls import path, include
from . import views

urlpatterns = [
    path('firstpage/', views.firstpage,name='firstpage'),
    path('secondpage/',views.secondpage,name='secondpage'),
    path('thirdpage/',views.thirdpage,name='thirdpage'),
]
