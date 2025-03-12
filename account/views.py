from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUser, UserProfileForm, ProfileForm
from .models import Profile, Account


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email , password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.info(request, "Your have been logged in sucessfully")
            return redirect("dashboard")
        else:
            messages.error(request, 'something went wrong')
            return redirect('login-page')
    return render (request, 'account/login-page.html')


def register_recruiter(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_recruiter = True
            user.username = user.email
            user.save()
            
            # Create a Profile instance for the user
            Profile.objects.create(user=user)
            
            messages.info(request, "Your account has been created successfully")
            return redirect('login-page')
        else:
            messages.error(request, "Something went wrong")
            return redirect('recruiter-page')
    else:
        form = RegisterUser()
        context = {'form': form}
    return render (request, 'account/recruiter-page.html', context)

def register_applicant(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_applicant = True
            user.username = user.email
            user.save()
            
            # Create a Profile instance for the user
            Profile.objects.create(user=user)
            
            messages.info(request, "Your account has been created successfully")
            return redirect('login-page')
        else:
            messages.error(request, "Something went wrong")
            return redirect('applicant-page')
    else:
        form = RegisterUser()
        context = {'form': form}
    return render (request, 'account/applicant-page.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, 'You have successfully logged out of your account')
    return redirect('home-page')

@login_required
def update_profile(request):
    account_form = UserProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        account_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile = profile_form.save(commit=False)
            profile.complete_profile = True
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')  # Redirect to dashboard or another page

    context = {
        'account_form': account_form,
        'profile_form': profile_form,
        
    }
    return render(request, 'account/update-profile.html', context)

# User Profile Details View
@login_required
def profile_detail(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/profile-details.html', {'profile': profile})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Delete the user account along with the profile due to cascading
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home-page')  # Redirect to the home page or login page
    return render(request, 'account/delete-account.html')  # Confirmation page