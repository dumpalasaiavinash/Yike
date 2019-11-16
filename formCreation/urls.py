from django.urls import path, include
from . import views

app_name = 'form'

urlpatterns = [
    path('main/',views.formCreateMain, name='form_main'),
    path('test/',views.testF, name='form_test')
]
