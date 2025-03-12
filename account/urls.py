from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login-page'),
    path('logout_user', views.logout_user, name='logout-page'),
    path('register_applicant/', views.register_applicant, name='applicant-page'),
    path('register_recruiter', views.register_recruiter, name='recruiter-page'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile_detail/', views.profile_detail, name='profile_details'),
    path('delete-account/', views.delete_account, name='delete-account'),
]