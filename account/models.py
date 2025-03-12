from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator

# Create your models here.
class Account(AbstractUser):
    email = models.EmailField(unique=True)
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)
    has_resume = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500,)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], blank=True)
    address = models.CharField(max_length=255,)
    firstname = models.CharField(max_length=255,)
    lastname = models.CharField(max_length=255,)
    username = models.CharField(max_length=255,)
    city = models.CharField(max_length=50,)
    country = models.CharField(max_length=50,)
    created_at = models.DateTimeField(auto_now_add=True)
    complete_profile = models.BooleanField(default=False)
    job_alerts = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    @property
    def completion_percentage(self):
        fields = [
            self.profile_picture,
            self.bio,
            self.firstname,
            self.username,
            self.lastname,
            self.phone_number,
            self.address,
            self.city,
            self.country,
        ]
        completed_fields = sum(1 for field in fields if field)
        total_fields = len(fields)
        return int((completed_fields / total_fields) * 100) if total_fields > 0 else 0