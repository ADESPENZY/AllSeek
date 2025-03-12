from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from job.models import Application, Job
from account.models import Account
from django.contrib import messages
from .models import Notification
from django.contrib.auth.decorators import login_required

@receiver(post_save, sender=Application)
def notify_recruiter_on_application(sender, instance, created, **kwargs):
    if created:  # Only notify for new applications
        Notification.objects.create(
            user=instance.job.user,  # Recruiter
            title="New Job Application",
            message=f"{instance.user.username} applied for your job: {instance.job.title}.",
            url=f"/job/jobs/{instance.job.id}/applications/"  # Correct URL for applications list
        )

@receiver(post_save, sender=Application)
def notify_applicant_on_status_change(sender, instance, **kwargs):
    Notification.objects.create(
        user=instance.user,  # Applicant
        title="Application Status Updated",
        message=f"Your application for {instance.job.title} is now {instance.status}.",
        url=f"/job/detail/{instance.job.id}/"  # Correct URL for job details
    )

@receiver(post_save, sender=Job)
def notify_applicants_on_new_job(sender, instance, created, **kwargs):
    if created:  # Only notify for new jobs
        # Assuming you have a list of users who are "subscribed" to job alerts
        interested_users = Account.objects.filter(profile__job_alerts=True)  # Adjust as per your implementation
        for user in interested_users:
            Notification.objects.create(
                user=user,
                title="New Job Posted",
                message=f"A new job '{instance.title}' has been posted.",
                url=f"/job/detail/{instance.id}/"  # Link to job details
            )

def notifications(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view notifications.")
        return redirect('home-page')  # Redirect to the dashboard or an appropriate page
    
    user_notifications = request.user.notifications.all().order_by('-created_at')
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'notification/notification.html', {
        'notifications': user_notifications,
        'unread_notifications_count': unread_notifications_count
    })

def mark_as_read(request, notification_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view notifications.")
        return redirect('home-page')  # Redirect to the dashboard or an appropriate page
    
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    next_url = request.GET.get('next', notification.url or 'notifications:list')
    return redirect(next_url)  # Redirect to the specified URL or the notification list

