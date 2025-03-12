from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_company, name='create_company'),
    path('update/<int:company_id>/', views.update_company, name='update-company'),
    path('delete/<int:company_id>/', views.delete_company, name='delete_company'),
    path('details/<int:company_id>/', views.company_details, name='company_details'),
    path('list/', views.company_list, name='company_list'),
]
