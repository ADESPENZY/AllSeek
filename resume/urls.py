from django.urls import path
from . import views

urlpatterns = [
    path('create_resume/', views.create_resume, name='create_resume'),
    path('update_resume/', views.update_resume, name='update_resume'),
    path('applicant_details/', views.applicant_details, name='applicant_details'),
    path('resume/delete/', views.delete_resume, name='delete-resume'),
    path('resume_pdf', views.resume_pdf, name='resume_pdf'),

]