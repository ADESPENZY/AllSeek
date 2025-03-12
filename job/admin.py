from django.contrib import admin
from .models import Job, Application

# Inline for Applications within a Job
class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0  # No extra blank fields
    readonly_fields = ('user', 'cover_letter', 'resume', 'applied_on', 'status')
    can_delete = False  # Prevent deletion from inline

# Admin for Jobs
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'is_available', 'create_date')  # List view
    list_filter = ('job_type', 'company', 'is_available', 'create_date')  # Filters
    search_fields = ('title', 'company__name', 'location', 'description')  # Searchable fields
    ordering = ('-create_date',)  # Default ordering
    list_editable = ('is_available',)  # Inline editing
    readonly_fields = ('create_date',)  # Read-only fields
    inlines = [ApplicationInline]  # Applications inline
    fieldsets = (
        (None, {
            'fields': ('user', 'company', 'title', 'location', 'job_type', 'is_available')
        }),
        ('Job Details', {
            'fields': ('description', 'requirement', 'responsibility', 'skills', 'salary_min', 'salary_max')
        }),
        ('Dates', {
            'fields': ('create_date',),
        }),
    )

# Admin for Applications
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_on', 'status')  # List view
    list_filter = ('status', 'applied_on')  # Filters
    search_fields = ('user__username', 'job__title')  # Searchable fields
    readonly_fields = ('applied_on',)  # Read-only fields
    ordering = ('-applied_on',)  # Default ordering
    fieldsets = (
        (None, {
            'fields': ('user', 'job', 'cover_letter', 'resume', 'status')
        }),
        ('Dates', {
            'fields': ('applied_on',),
        }),
    )
