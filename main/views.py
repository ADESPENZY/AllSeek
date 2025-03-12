from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from job.models import Job  # Import Job model

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from job.models import Job  # Import Job model

def home(request):
    # Search and filter queries
    job_query = request.GET.get('job', '').strip()  # Search query for job title or company
    location_query = request.GET.get('location', '').strip()  # Location filter
    job_id = request.GET.get('job_id')  # Selected job ID

    # Query all available jobs
    jobs = Job.objects.filter(is_available=True)

    # Apply filters based on search query
    if job_query:
        jobs = jobs.filter(
            Q(title__icontains=job_query) | Q(company__name__icontains=job_query)
        )
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    # Pagination for job listings
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    # Recommended jobs (excluding the jobs on the current page)
    recommended_jobs = Job.objects.filter(is_available=True).exclude(
        id__in=jobs_page.object_list.values_list('id', flat=True)
    )[:5]

    # Fetch the selected job details
    selected_job = None
    if job_id:
        selected_job = get_object_or_404(Job, id=job_id)

    # Context data for the template
    context = {
        'jobs': jobs_page,
        'job_query': job_query,
        'location_query': location_query,
        'selected_job': selected_job,
    }
    return render(request, 'main/home_page.html', context)

def banner(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already registered.")
        # Redirect to the dashboard
        return redirect('dashboard')
    return render(request, 'main/banner_page.html')

def resume_view(request):
    return render(request, 'main/resume_view.html')

def settings(request):
    return render(request, 'main/settings.html')

from django.http import JsonResponse
from job.models import Job

def fetch_job_details(request):
    job_id = request.GET.get('job_id')  # Get job_id from query parameter
    if job_id is None:
        return JsonResponse({'error': 'job_id parameter is required'}, status=400)
    try:
        job = Job.objects.get(id=job_id)
        print(f"Job found: {job}")  # Debugging line to check if job is found
        job_data = {
            'title': job.title,
            'company': job.company.name,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'job_type': job.job_type,
            'description': job.description,
            'requirement': job.requirement,
            'responsibility': job.responsibility,
            'posted_date': job.create_date.strftime("%b %d, %Y")
        }
        return JsonResponse(job_data)
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)




