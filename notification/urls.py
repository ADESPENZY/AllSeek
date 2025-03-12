from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path('', views.notifications, name='list'),  # For listing all notifications
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark-as-read'),  # Mark a notification as read
]
