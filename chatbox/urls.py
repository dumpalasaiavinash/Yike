from django.urls import path, include
from . import views

urlpatterns = [
    path('chatbox/',views.con,name='index'),
    path('chat/',views.chat,name='chat'),
    path('msg/',views.msg,name='msg'),
    path('temp/',views.preview),
    path('recents/', views.recents),
    path('mesgs/',views.mesgs)

]
