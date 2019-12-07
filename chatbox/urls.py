from django.urls import path, include
from . import views

urlpatterns = [
    path('chat/',views.chat,name='chat'),
    path('msg/',views.msg00,name='msg'),
    path('temp/',views.preview),
    path('recents/', views.recents),
    path('mesgs/',views.mesgs),
    

]
