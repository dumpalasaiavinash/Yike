# from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'orgadmin'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/',views.create, name='create'),
    path('createform/',views.createform, name='createform'),
    path('departments/',views.departments, name='departments'),
    path('hierarchy//<dep_id>/',views.hierarchy, name='hierarchy'),
]
