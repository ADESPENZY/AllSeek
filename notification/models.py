from django.db import models
from account.models import Account

class Notification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # For in-app notifications
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)  # Optional: Link to relevant page (e.g., job detail)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"