# from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'orgadmin'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('dashboard/<int:j>', views.dashboard, name='dashboard'),
    path('activate/(?P<uidb64>[-a-zA-Z0-9_]+)/(?P<token>[-a-zA-Z0-9_]+)/(?P<user_id>[-a-zA-Z0-9_]+)/(?P<password>[-a-zA-Z0-9_]+)/(?P<org_id>[-a-zA-Z0-9_]+)',views.activate,name='activate'),
    path('delete_employee/<int:org_id>/<int:emp_id>',views.delete_employee,name='delete_employee'),
    path('create/',views.create, name='create'),
    path('created/',views.created, name='created'),
    path('join/',views.join, name='join'),
    path('createform/',views.createform, name='createform'),
    path('departments/',views.departments, name='departments'),

    path('hierarchy/',views.hierarchy, name='hierarchy'),
    path('departments_hierarchy_update/',views.departments_hierarchy_update, name='departments_hierarchy_update'),
    path('create_department/',views.create_department, name='create_department'),
    path('api', views.complaintrest.as_view(), name='api'),
    
]
