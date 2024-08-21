from django.db import models

# Create your models here.
class Company(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    job_description = models.TextField()
    job_url = models.URLField(max_length=200)
    company_url = models.URLField(max_length=200)
    job_posted_date = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title