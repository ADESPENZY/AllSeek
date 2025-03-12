from django import forms
from .models import Company

class UpdateCompany(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)  # The 'user' field is excluded as it's set programmatically
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'country': forms.Select(choices=Company.country_choices, attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'founded_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'industry': forms.Select(choices=Company.industry_choices, attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'size': forms.Select(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], attrs={'class': 'form-control'}),
            'recruitment_policy': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Recruitment Policy'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_recruit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter URL'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram URL'}),
            'founder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Founder Name'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'about'}),
            'mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'mission'}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'vision'}),
        }
