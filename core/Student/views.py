from django.shortcuts import render,redirect
from django.contrib import messages
from core.models import *



def home(request):
    user=request.user
    return render(request,'Student/home.html',{"user":user})