from django import forms
from job.models import Job, Application
from company.models import Company

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'create_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Salary'}),
            'requirement': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Requirements', 'rows': 4}),
            'responsibility': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Responsibilities', 'rows': 4}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Skills Required', 'rows': 4}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Dynamically filter company dropdown based on the logged-in user
        if user:
            self.fields['company'].queryset = Company.objects.filter(user=user)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
