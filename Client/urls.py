from django.urls import path, include
from . import views

urlpatterns = [
    path('firstpage/', views.firstpage,name='firstpage'),
    path('secondpage/',views.secondpage,name='secondpage'),
    path('thirdpage/',views.thirdpage,name='thirdpage'),
    path('track/',views.track,name='track'),
    path('signup/',views.client_signup,name='client_signup'),
    path('signin/',views.client_signin,name='client_signin'),
    path('login/',views.client_login,name='client_login'),
    path('loggedin/',views.client_loggedin,name='client_loggedin')
]
