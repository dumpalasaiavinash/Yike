from django.urls import path, include
from . import views
app_name = 'Client'

urlpatterns = [
    path('firstpage/', views.firstpage,name='firstpage'),
    path('secondpage/',views.secondpage,name='secondpage'),
    path('activate/(?P<token>[-a-zA-Z0-9_]+)/(?P<email>[-a-zA-Z0-9_]+)/(?P<username>[-a-zA-Z0-9_]+)/(?P<client_id>[-a-zA-Z0-9_]+)',views.activate,name='activate'),
    path('thirdpage/',views.thirdpage,name='thirdpage'),
    path('track/',views.track,name='track'),
    path('signup/',views.client_signup,name='client_signup'),
    path('signin/',views.client_signin,name='client_signin'),
    path('login/',views.client_login,name='client_login'),
    path('loggedin/',views.client_loggedin,name='client_loggedin'),
    path('email_verification/',views.email_verification,name='email_verification'),
    path('home/',views.client_home,name='client_home'),
    path('refresh/<int:client_id>/',views.refresh,name="refresh")
]
