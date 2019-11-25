from django.urls import path, include
from . import views

urlpatterns = [
    path('new_complaint_form/',views.complaint_form_add),
    path('orgs/',views.get_org),
    path('forms/',views.get_Complaint_Form),
    path('tokenpair/',views.getTokenPair),
    path('refreshtoken/',views.get_access_token),
    path('getMyComplaints/',views.myComplaintHistory),
    path('getComplaintDetails/', views.get_Complaint_Detail)
]