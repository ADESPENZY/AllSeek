from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateJobForm, ApplicationForm
from .models import Job, Application
from company.models import Company
from django.db.models import Q
from django.core.paginator import Paginator

# Recruiter: Create Job
@login_required
def create_job(request):
    if not request.user.is_recruiter:
        messages.error(request, "You do not have permission to post jobs.")
        return redirect('dashboard')

    if not request.user.has_company:
        messages.error(request, "You must have a company to create a job.")
        return redirect('dashboard')

    companies = Company.objects.filter(user=request.user)  # Only recruiter’s companies

    if request.method == 'POST':
        form = CreateJobForm(request.POST, user=request.user)  # Pass user to form
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('dashboard')
    else:
        form = CreateJobForm(user=request.user)  # Pass user to form

    context = {
        'form': form,
        'companies': companies,  # Pass filtered companies to the template if needed
    }
    return render(request, 'job/create_job.html', context)

# Recruiter: Update Job
@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, id=pk, user=request.user)
    if request.method == 'POST':
        form = CreateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('dashboard')
    else:
        form = CreateJobForm(instance=job)
    
    return render(request, 'job/update_job.html', {'form': form})

# Applicant: View Job Details
def job_detail(request, pk):  # Change job_id to pk
    job = get_object_or_404(Job, id=pk)  # Use pk here
    requirements = [req.strip() for req in job.requirement.split('\n') if req.strip()]  # Clean and split
    responsibilities = [res.strip() for res in job.responsibility.split('\n') if res.strip()] if job.responsibility else []
    return render(request, 'job/job_detail.html', {
        'job': job,
        'requirements': requirements,
        'responsibilities': responsibilities,
    })

def apply_job(request, pk):
    # Fetch the job based on the primary key (pk), ensuring it is available
    job = get_object_or_404(Job, id=pk, is_available=True)

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to apply for job.")
        return redirect('home-page')  # Redirect to the dashboard or an appropriate page
    
    # Ensure the user is an applicant
    if not request.user.is_applicant:
        messages.warning(request, "You must be an applicant to apply for jobs.")
        return redirect('dashboard')  # Redirect to the dashboard or an appropriate page

    # Check if the user's profile is complete
    profile = request.user.profile
    if not profile.complete_profile:
        messages.warning(request, "Please complete your profile before applying for a job.")
        return redirect('dashboard')  # Redirect to the dashboard for profile completion
    
    # Check if the user has already applied for this job
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('home-page')

    # Handle POST request for job application
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Link the application to the current user
            application.job = job  # Link the application to the job
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = ApplicationForm()  # Empty form for GET request

    # Render the application form page
    return render(request, 'job/apply_job.html', {'form': form, 'job': job})

# Applicant: View All Applications
@login_required
def view_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'job/applicant_app_views.html', {'applications': applications})

# Recruiter: Approving Rejecting Job
@login_required
def view_applications_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    applications = Application.objects.filter(job=job)

    if request.method == "POST":
        application_id = request.POST.get("application_id")
        new_status = request.POST.get("status")
        print(f"Application ID: {application_id}, Status: {new_status}")  # Debugging line

        # Update application status
        application = get_object_or_404(Application, id=application_id, job=job)
        if new_status in ["PENDING", "APPROVED", "REJECTED"]:
            application.status = new_status
            application.save()
            messages.success(request, f"Application status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status update.")

        return redirect('view-applications', job_id=job.id)

    return render(request, 'job/view_applications.html', {'job': job, 'applications': applications})

# def view_applications_for_job(request, job_id):
#     job = get_object_or_404(Job, id=job_id, user=request.user)
#     applications = Application.objects.filter(job=job)
#     print(applications)  # Debugging line
#     return render(request, 'job/view_applications.html', {'applications': applications})


def view_jobs(request):
    my_jobs = Job.objects.filter(user=request.user)
    return render(request, 'job/my_jobs.html', {'my_jobs': my_jobs})

def delete_job(request, pk):
    jobs = get_object_or_404(Job, id=pk, user=request.user)
    if request.method == 'POST':
        jobs.delete()
        messages.success(request, "Company deleted successfully!")
        return redirect('dashboard')  # Redirect after deletion
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'job/delete_job.html', context)

@login_required
def toggle_job_status(request, pk):
    job = get_object_or_404(Job, id=pk, user=request.user)
    job.is_available = not job.is_available
    job.save()
    status = "available" if job.is_available else "unavailable"
    messages.success(request, f"Job is now marked as {status}.")
    return redirect('view-jobs')  # Redirect to the recruiter's job list

def withdraw_application(request, id):
    application = Application.objects.get(id=id)
    if application.user == request.user:
        application.delete()  # Withdraw the application
        messages.success(request, "Application withdrawn successfully.")
    else:
        messages.error(request, "You cannot withdraw this application.")
    return redirect('dashboard')

