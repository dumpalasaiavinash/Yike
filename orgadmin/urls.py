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
    path('pre_create/',views.pre_create, name='pre_create'),    
    path('created/',views.created, name='created'),
    path('join/',views.join, name='join'),
    path('createform/',views.createform, name='createform'),
    path('departments/',views.departments, name='departments'),
    path('about/<int:org_id>',views.about,name='about'),
    path('hierarchy/',views.hierarchy, name='hierarchy'),
    path('departments_hierarchy_update/',views.departments_hierarchy_update, name='departments_hierarchy_update'),
    path('create_department/',views.create_department, name='create_department'),
    path('remove_department/',views.remove_department, name='remove_department'),
    path('api/', views.complaintrest.as_view(), name='api'),
    path('about_name_edit/<int:org_id>',views.about_name_edit,name='about_name_edit'),
    path('about_info_edit/<int:org_id>',views.about_info_edit,name='about_info_edit'),
    path('about_image_edit/<int:org_id>',views.about_image_edit,name='about_image_edit'),
    path('test/123',views.test,name='test'),

]
