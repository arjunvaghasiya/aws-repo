from django.db import models
from django.contrib.auth.models import User, BaseUserManager

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_address = models.CharField(max_length=400, blank=True)
    permenent_addresss = models.CharField(max_length=400, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, blank=True)
    dte_of_bir = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)


class CompanyDetails(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    designation = models.CharField(max_length=400, blank=True)
    experience = models.CharField(max_length=400, blank=True)
    branch_code = models.CharField(max_length=400, blank=True)
    project_manager = models.CharField(max_length=400, blank=True)
    working_project = models.CharField(max_length=400, blank=True)
    salary = models.FloatField(null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return str(self.profile)
