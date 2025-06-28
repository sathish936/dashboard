from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True) 
    email = models.EmailField()  # optional field
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    contact = models.CharField(max_length=20)
    achievements = models.TextField(blank=True)
    department = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    contact = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
