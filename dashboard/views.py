from django.shortcuts import render, redirect
from company.models import Company
from resume.models import Resume
from account.models import Profile
from job.models import Job, Application
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login-page')  # Replace 'login' with the name of your login URL pattern

    companies = Company.objects.filter(user=request.user)  # Queryset of companies
    jobs = Job.objects.filter(user=request.user).order_by('-create_date')[:3]  # Queryset of jobs
    resume = Resume.objects.filter(user=request.user).first()
    profile = Profile.objects.filter(user=request.user).first()
    applied_jobs = Application.objects.filter(user=request.user)

    return render(request, 'dashboard/dashboard.html', {
        'companies': companies,
        'resume': resume,
        'profile': profile,
        'jobs': jobs,
        'applied_jobs': applied_jobs,
    })


def manage_jobs(request):
    jobs = Job.objects.filter(user=request.user)  # Ensure this returns valid Job objects
    return render(request, 'dashboard/manage_jobs.html', {'jobs': jobs})

