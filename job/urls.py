from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),  # Recruiter creates a job
    path('update/<int:pk>/', views.update_job, name='update_job'),  # Recruiter updates a job
    path('detail/<int:pk>/', views.job_detail, name='job_detail'),  # View job details
    path('delete/<int:pk>/', views.delete_job, name='delete_job'),  # View job details
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),  # Applicant applies for a job
    path('applications/', views.view_applications, name='applicant_view_app'),  # Applicant views their applications
    path('view-jobs/', views.view_jobs, name='view-jobs'),
    path('toggle-job-status/<int:pk>/', views.toggle_job_status, name='toggle-job-status'),
    path('jobs/<int:job_id>/applications/', views.view_applications_for_job, name='view-applications'),
    path('withdraw-application/<int:id>/', views.withdraw_application, name='withdraw_application'),
]
