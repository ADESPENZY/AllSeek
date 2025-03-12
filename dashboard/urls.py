from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manage_jobs/', views.manage_jobs, name='manage_jobs'),
]