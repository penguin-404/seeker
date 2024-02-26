from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User,job_post

class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, label='company_name')
    industry = forms.CharField(max_length=100, label='industry')
    location = forms.CharField(max_length=100, label='location')

    class Meta:
        model = User
        fields = ['username','company_name','password1', 'password2', 'industry','location']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.company_name = self.cleaned_data['company_name']
        user.industry = self.cleaned_data['industry']
        user.location = self.cleaned_data['location']
        user.is_company = True
        if commit:
            user.save()
        return user

class ApplicantRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label='Full Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.is_applicant = True
        if commit:
            user.save()
        return user

class JobForm(ModelForm):
    class Meta:
        model = job_post
        fields = ['title', 'company', 'description']
