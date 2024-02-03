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

class job_post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    company_id = models.FloatField(null=True, blank=True)
    education = models.CharField(max_length=255)
    description = models.TextField()