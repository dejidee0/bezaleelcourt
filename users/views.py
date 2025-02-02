import os
import uuid
from property import settings

from django.shortcuts import render, redirect
from supabase import create_client
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CustomUser


SUPABASE_STORAGE_BUCKET = "media"

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES.get('profile_picture', None)
        address = request.POST['address']
        bio = request.POST['bio']
        email = request.POST['email'].lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        file_url = None  # Default to None if no image is uploaded

        if profile_picture:
            # Generate a unique file name
            file_name = f"profiles/{uuid.uuid4()}_{profile_picture.name}"

            # Upload to Supabase Storage
            response = settings.supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(file_name, profile_picture.read())


            # Generate public URL
            file_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}/{file_name}"

        # Validate Password
        if password == confirm_password:
            if CustomUser.objects.filter(username=email).exists():
                messages.error(request, 'Email already exists.')
            elif not phone_number:
                messages.error(request, 'Phone number is required.')
            else:
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    profile_picture=file_url,  # Save the Supabase image URL
                    address=address,
                    bio=bio,
                    username=email,
                    email=email, 
                    password=password
                )
                user.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')


def custom_login_view(request):
    """
    A custom login view to handle login requests manually.
    """
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return redirect("dashboard")  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    
    return render(request, 'login.html')
