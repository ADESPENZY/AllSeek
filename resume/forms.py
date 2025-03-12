from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user',)  # Exclude user field as it's set programmatically
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Add the file field with a file input widget
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Religion'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School Name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification'}),
            'year_of_graduation': forms.NumberInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control','rows': 4,'placeholder': 'Describe your work experience','help_text': 'Include key roles and responsibilities'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Skills'}),
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'References', 'required': False}),
        }
