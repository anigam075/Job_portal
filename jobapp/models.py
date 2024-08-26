from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    job_description = models.TextField()
    job_url = models.CharField(max_length=1000)
    company_url = models.CharField(max_length=1000)
    job_posted_date = models.CharField(max_length=255)
    is_deleted = models.CharField(max_length=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    resume_link = models.CharField(max_length=1000, blank=True, null=True)
    is_deleted = models.CharField(max_length=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=100)
    start_date = models.CharField(max_length=11, null=True, blank=True)
    end_date = models.CharField(max_length=11, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.CharField(max_length=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.job_title} at {self.company_name}'

class EducationData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, null=True, blank=True)
    college = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.CharField(max_length=11, null=True, blank=True)
    end_date = models.CharField(max_length=11, null=True, blank=True)
    is_deleted = models.CharField(max_length=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.degree} at {self.college}'