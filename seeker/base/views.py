from decimal import Decimal
import json
from django.shortcuts import get_object_or_404, render,redirect
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login,logout
from .forms import ApplicantRegistrationForm,CompanyRegistrationForm,JobForm
from django.contrib import messages
from .models import Applicant,Company,job_post,UserProfile,Bid
from django.http import JsonResponse
from .models import JobApplication,job_post
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
def applicant_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Check user type
        user_type = request.POST.get('user_type')
        if user_type == 'applicant':
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_applicant:
                login(request, user)
                return redirect('user-dashboard')
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
            return redirect('create-profile')
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
def logoutpage(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def index(request):
    return render(request,'base/index.html')
def find_work(request):
    jobs = job_post.objects.all()[:50] 
    job_count = jobs.count()
    context = {'jobs':jobs,'job_count':job_count}
    return render(request,'base/find-work.html',context)
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
    if not (request.user.is_authenticated and request.user.is_company and request.user.company.user == job.company):
        return HttpResponse("You do not have permission to access this page.")
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

def apply_for_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        applicant = request.user.applicant
        try:
            # Create a new JobApplication instance
            job_application = JobApplication.objects.create(job_post_id=job_id,applicant=applicant)
            job = get_object_or_404(job_post, pk=job_id)
            salary = job.salary
            lower_bound = salary * Decimal('0.8')
            upper_bound = salary * Decimal('1.2')
            context = {'job':job,'lower_bound': lower_bound,'upper_bound':upper_bound}
            return render(request,'base/bid.html',context)
            # return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def process_bid(request):
    if request.method == 'POST':
        bid_amount = request.POST.get('bid-amount')
        job_id = request.POST.get('job_id')
        try:
            print(bid_amount)
            bid = Bid.objects.create(amount=bid_amount, job_post_id=job_id)
            return JsonResponse({'success': True, 'message': 'Bid submitted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
def user_dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    print(profile)
    recommendations = None  # Define recommendations variable outside the if block
    def build_request_data():
        return {
            "id": profile.profile_id,
            "position": profile.interests,
            "skills": profile.skills,
            "education": profile.education,
            "location": profile.location
        }
    data = build_request_data()
    response = requests.post('http://127.0.0.1:8000/recommend', json=data)
    if response.status_code == 200:
        recommendations = response.json()
        job_recommendations = []
    for i in range(len(recommendations['ID'])):
        job = {
        'ID': recommendations['ID'][str(i)],
        'title': recommendations['title'][str(i)],
        'company': recommendations['company'][str(i)],
        'location': recommendations['location'][str(i)],
        'description': recommendations['description'][str(i)]
        }
        job_recommendations.append(job)
    print(job_recommendations)
    jobs = job_post.objects.all()
    job_count = jobs.count()
    context = {'jobs':jobs,'job_count':job_count,'job_recommendations':job_recommendations,'profile':profile}
    return render(request,'base/user-dashboard.html',context)

def create_profile(request):
    if request.method == 'POST':
        # Check if the user already has a profile
        if not UserProfile.objects.filter(user=request.user).exists():
            interests = request.POST.get('interests')
            skills = request.POST.get('skills')
            location = request.POST.get('location')
            education = request.POST.get('education')
            profile = UserProfile(user=request.user, interests=interests, skills=skills, education=education,location=location)
            profile.save()
            return redirect('profile',pk=profile.profile_id)
        else:
            print("Profile already exists")
            pass
    return render(request, 'base/create-profile.html')
def edit_profile(request):
    # Get the existing profile if it exists
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        # Update profile data with the submitted form data
        profile.interests = request.POST.get('interests')
        profile.skills = request.POST.get('skills')
        profile.education = request.POST.get('educationLevel')
        profile.save()
        # Redirect to profile page after editing
        return redirect('profile', pk=profile.profile_id)
    
    # Pass the existing profile data to the template for editing
    context = {
        'profile': profile
    }
    return render(request, 'base/create-profile.html', context)
def profile_view(request, pk):
    try:
        # Try to retrieve the UserProfile based on the provided pk
        profile = UserProfile.objects.get(profile_id=pk)
        # If the profile exists, render the profile page
        return render(request, 'base/profile.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        # If the profile does not exist, redirect to the profile creation page
        return redirect('create-profile')
    except Exception as e:
        print(f"An error occurred while retrieving profile: {e}")
        raise Http404("Profile not found")