from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Profile

class RegisterUser(UserCreationForm):
    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter your email'
        })
    )
    
    password1 = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Enter a password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password:",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            'placeholder': 'Re-enter your password'
        })
    )
    class Meta:
        model = Account
        fields = ['email','password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email']  # Allow users to edit email
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your email'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname', 'lastname', 'username', 'bio', 'profile_picture',
            'phone_number', 'address', 'city', 'country'
        ]
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Firstname'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Lastname'
            }),
            'username': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Username'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Tell us about yourself',
                'rows': 4
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Phone Number'
            }),
            'address': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your City'
            }),
            'country': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-600',
                'placeholder': 'Enter your Country'
            }),
        }