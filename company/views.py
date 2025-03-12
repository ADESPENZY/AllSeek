from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .forms import UpdateCompany
from django.contrib import messages
from account.models import Account

# Create your views here.
def create_company(request):
    if request.user.is_recruiter:
        if request.method == 'POST':
            form = UpdateCompany(request.POST, request.FILES)
            if form.is_valid():
                company = form.save(commit=False)
                company.user = request.user
                company.save()
                request.user.has_company = True
                request.user.save()
                messages.success(request, "Company created successfully!")
                return redirect('dashboard')  # Redirect to the dashboard
        else:
            form = UpdateCompany()
        
        context = {'form': form}
        return render(request, 'company/create-company.html', context)
    else:
        messages.error(request, "You are not authorized to create a company.")
        return redirect('banner-page')

def update_company(request, company_id):
    # Check if the user is authorized
    if not getattr(request.user, "is_recruiter", False):
        messages.error(request, "You are not authorized to update a company.")
        return redirect('banner-page')
    
    # Fetch the company by ID, ensuring it belongs to the logged-in user
    company = get_object_or_404(Company, id=company_id, user=request.user)

    if request.method == 'POST':
        form = UpdateCompany(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company updated successfully!")
            return redirect('dashboard')  # Redirect after successful update
        else:
            print(form.errors)  # Debugging: Print form errors
    else:
        form = UpdateCompany(instance=company)
    
    context = {
        'form': form,
        'company': company,
    }
    return render(request, 'company/update-company.html', context)

def delete_company(request, company_id):
    if not request.user.is_recruiter:
        messages.error(request, "You are not authorized to delete a company.")
        return redirect('banner-page')
    
    company = get_object_or_404(Company, id=company_id, user=request.user)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company deleted successfully!")
        return redirect('dashboard')  # Redirect after deletion
    
    context = {
        'company': company,
    }
    return render(request, 'company/delete-company.html', context)

def company_details(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    context = {
        'company': company,
    }
    return render(request, 'company/company-details.html', context)

def company_list(request):
    if not request.user.is_recruiter:
        messages.error(request, "You are not authorized to view companies.")
        return redirect('banner-page')
    
    companies = Company.objects.filter(user=request.user)  # Only show companies created by the logged-in recruiter
    
    context = {
        'companies': companies,
    }
    return render(request, 'company/company-list.html', context)