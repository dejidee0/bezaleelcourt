from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager



class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    You can add additional fields as needed.
    """
    email = models.EmailField(unique=True)  # Enforce unique emails
    is_verified = models.BooleanField(default=False)  # User verification status
    phone_number = models.CharField(max_length=15, blank=False, null=False)  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Optional profile picture
    bio = models.TextField(blank=True, null=True)  # Optional bio field
    
    def __str__(self):
        return self.username
