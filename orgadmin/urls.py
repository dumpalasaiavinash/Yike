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
    path('hierarchy/',views.hierarchy, name='hierarchy'),
    path('departments_hierarchy_update/<hierarchy>',views.departments_hierarchy_update, name='departments_hierarchy_update'),
]
