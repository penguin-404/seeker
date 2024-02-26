# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_applicant = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    # Add related_name to avoid clashes with default User model
User._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'
class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # company_id = models.CharField(max_length=255)
    # name = models.CharField(max_length=255,default=None)
    # location = models.CharField(max_length=255,default=None)

class job_post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    company_id = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255)
    description = models.TextField()

class JobApplication(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job_post = models.ForeignKey(job_post, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Bid(models.Model):
    job_post = models.ForeignKey(job_post, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid for {self.job_post.title} - Amount: {self.amount}"
class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField()
    education = models.CharField(max_length=255)
    location = models.CharField(max_length=255,default='ktm')
    interests = models.TextField()

    def __str__(self):
        return f"Profile of {self.user.username}"