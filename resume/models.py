from django.db import models
from account.models import Account
from django.core.validators import FileExtensionValidator
import os
from uuid import uuid4

# Function to handle file uploads with unique names
def upload_resume_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('resumes/files/', filename)

class Resume(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    ]

    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='resume_image', 
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], 
        null=True, blank=True
    )
    file = models.FileField(
        upload_to='resumes/files/',
        validators=[FileExtensionValidator(['pdf', 'docx'])],
        null=True,
        blank=True,
        help_text="Upload your resume as a PDF or Word document."
    )
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='None')
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)  # Ensure this exists

    # Educational details
    school = models.CharField(max_length=200, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    year_of_graduation = models.IntegerField(null=True, blank=True)

    # Work Experience
    experience = models.TextField(null=True, blank=True)

    # Skills
    skills = models.TextField(null=True, blank=True)

    # References
    reference = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}'s Resume"
