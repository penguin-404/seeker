from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import ApplicantRegistrationForm,CompanyRegistrationForm,JobForm
from django.contrib import messages
from .models import Applicant,Company,job_post
def applicant_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        if user_type == 'applicant':
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_applicant:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid user type.')

    return render(request, 'base/user-login.html')
def applicant_registration_view(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            applicant = Applicant(user=user)
            applicant.save() 
            messages.success(request, f'Account created successfully for {user.username}')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Error during form submission. Please check your data.')
    else:
        form = ApplicantRegistrationForm()

    return render(request, 'base/user-register.html', {'form': form})

def company_registration_view(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            company = Company(user=user)
            company.save()
            messages.success(request, f'Account created successfully for {user.username}')
            login(request, user)
            return redirect('company-dashboard')
        else:
            messages.error(request, 'Error during form submission. Please check your data.')
    else:
        form = CompanyRegistrationForm()

    return render(request, 'base/company-register.html', {'form': form})

def company_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Check user type
        user_type = request.POST.get('user_type')
        if user_type == 'company':
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_company:
                login(request, user)
                return redirect('company-dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid user type.')

    return render(request, 'base/company-login.html')

def index(request):
    return render(request,'base/index.html')

def create_job(request):
    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('index')
            except Exception as e:
                print(f"Error saving job post: {e}")
                # Handle the error as needed
        else:
            print(f"Form is not valid: {form.errors}")
    jobs = job_post.objects.all()
    job_count = jobs.count()
    context = {'form':form,'jobs':jobs,'job_count':job_count}
    return render(request,'base/company-dashboard.html',context)
def update_job(request,pk):
    job = job_post.objects.get(id=pk)
    form = JobForm(instance=job)
    if request.method == 'POST':
        form = JobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form}
    return render(request,'base/company-dashboard.html',context)

def delete_job(request, pk):
    job = job_post.objects.get(id=pk)

    if request.method == 'POST':
        job.delete()
        return redirect('index')
    return render(request, 'base/delete.html', {'obj': job})