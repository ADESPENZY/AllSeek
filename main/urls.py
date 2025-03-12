from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('banner/', views.banner, name='banner-page'),
    path('settings/', views.settings, name='settings-page'),
    path('resume_view/', views.resume_view, name='resume-view-page'),
    
    path('fetch-job-details/', views.fetch_job_details, name='fetch_job_details'),

]