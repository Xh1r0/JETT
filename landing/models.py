from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# ======================
# 🧑 Custom User Model
# ======================
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = None  # kita tidak pakai username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


# ======================
# ✉️ Email Verification
# ======================
class EmailVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verifikasi untuk {self.user.full_name}"


# ======================
# 🏢 Company Model
# ======================
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ======================
# 💼 Job Model
# ======================
class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship')
    ])
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"


# ======================
# 🧾 Applicant Model
# ======================
class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.job.title})"
