from django.urls import path, include
from . import views


urlpatterns = [
    path('main/',views.formCreateMain),
    path('test/',views.testF)
]
