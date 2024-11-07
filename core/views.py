from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from core.models import *
from django.contrib import messages

def login_page(request):
    user = request.user
    if user.is_authenticated:
        
        if user.is_superuser:
            
            return redirect('admin:index')
        # Redirect based on user role if authenticated
        if Administrator.objects.filter(user=user).exists():
            return redirect('administration:home')
        elif Lecturer.objects.filter(user=user).exists():
            return redirect('lecturer:home')
        elif Student.objects.filter(user=user).exists():
            return redirect('student:home')
        else:
            # Optional: handle case if authenticated user doesn't match any role
            messages.warning(request, "User role not recognized.")
            return redirect('login')  # Or another suitable page
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
            
              return redirect('admin:index')
            # Redirect based on user role after successful login
            if Administrator.objects.filter(user=user).exists():
                return redirect('administration:home')
            elif Lecturer.objects.filter(user=user).exists():
                return redirect('lecturer:home')
            elif Student.objects.filter(user=user).exists():
                return redirect('student:home')
        else:
            # Authentication failed: show warning message and redirect to login
            messages.warning(request, "Username or Password incorrect. Please check again.")
            return redirect('login')
    
    # Render login page if GET request or no other conditions met
    return render(request, 'login.html', {})
