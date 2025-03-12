from django.contrib import admin
from .models import Account, Profile

# Account Admin
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_recruiter', 'is_applicant', 'has_company', 'has_resume')
    list_filter = ('is_recruiter', 'is_applicant', 'has_company', 'has_resume')
    search_fields = ('email', 'username')
    ordering = ('email',)

# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_email', 'firstname', 'lastname', 'city', 'country', 'complete_profile', 'completion_percentage')
    list_filter = ('complete_profile', 'job_alerts', 'country', 'city')
    search_fields = ('user__email', 'firstname', 'lastname', 'city', 'country')
    readonly_fields = ('created_at', 'completion_percentage')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'firstname', 'lastname', 'username', 'phone_number')
        }),
        ('Profile Details', {
            'fields': ('profile_picture', 'bio', 'address', 'city', 'country')
        }),
        ('Settings', {
            'fields': ('complete_profile', 'job_alerts', 'created_at', 'completion_percentage')
        }),
    )

    # Custom method to display the email
    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
