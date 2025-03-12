from django.db import models
from account.models import Account
from company.models import Company

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('REMOTE', 'Remote'),
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
        ('FREELANCE', 'Freelance'),
    ]
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='jobs')  # Recruiter
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField('Job Title', max_length=200, unique=True)
    location = models.CharField('Location', max_length=200,)
    job_type = models.CharField(max_length=20,choices=JOB_TYPE_CHOICES,default='FULL_TIME',)
    salary_min = models.PositiveIntegerField('Salary', default=70000)
    salary_max = models.PositiveIntegerField('Salary', default=100000)
    requirement = models.TextField('Requirements')
    responsibility = models.TextField('Responsibilities')
    description = models.TextField('Job Description', null=True, blank=True)
    skills = models.TextField('Skills')
    is_available = models.BooleanField(default=False)
    create_date = models.DateTimeField('Posted On', auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled Job"

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='applications')  # Applicant
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField('Cover Letter', blank=True)
    resume = models.FileField('Resume', upload_to='resumes/', blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')  # New Field

    def __str__(self):
        return f"Application by {self.user} for {self.job.title}"
