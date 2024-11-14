from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from core.models import *
from core.Administration import forms
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    user=request.user
    return render(request,'Administration/home.html',{"user":user})

@login_required
def createclass(request):
    departments = Department.objects.all()  # Fetch all departments for the dropdown
    if request.method == "POST":
        user = request.user
        speciality = request.POST["speciality"]
        department_name = request.POST['department']  # Department name from form input
        classcode = request.POST['classcode']
        level = request.POST['level']
        creator = Administrator.objects.get(user=user)
        
        try:
            # Get department instance based on the selected department name
            department_instance = Department.objects.get(departmentname=department_name)
            
            # Create a new Classe instance with the provided information
            Classe.objects.create(
                creator=creator,
                classcode=classcode,
                department=department_instance,
                level=level,
                speciality=speciality
            )
            messages.success(request, 'Class is added successfully')
            return redirect(reverse('administration:classes'))
        
        except Department.DoesNotExist:
            messages.error(request, "Selected department does not exist.")
            return redirect(reverse('administration:classes'))
        
    else:
        return render(request, 'administration/add_class.html', {'departments': departments})  
    
@login_required   
def classes(request):
    classe=Classe.objects.all
    return render(request,'administration/manageclass.html',{"classe":classe})

@login_required
def moreinfoclass(request,id):
    classe=Classe.objects.get(id=id)
    return render(request,'administration/viewclass.html',{"classe":classe})

@login_required
def updateclass(request, id):
    # Get all departments to populate the department dropdown
    departments = Department.objects.all()

    # Retrieve the class object you want to edit
    try:
        classe = Classe.objects.get(id=id)
    except Classe.DoesNotExist:
        messages.error(request, "Class not found.")
        return redirect(reverse('administration:classes'))

    if request.method == "POST":
        # Get the currently logged-in user
        user = request.user

        # Extract form data
        speciality = request.POST["speciality"]
        department_name = request.POST["department"]
        classcode = request.POST["classcode"]
        level = request.POST["level"]

        # Get the creator (Administrator)
        creator = Administrator.objects.get(user=user)

        # Get the department from the database using the department name
        try:
            department = Department.objects.get(departmentname=department_name)
        except Department.DoesNotExist:
            messages.error(request, "Department not found.")
            return redirect(reverse('administration:classes'))

        # Update the existing class object
        classe.speciality = speciality
        classe.department = department
        classe.classcode = classcode
        classe.level = level
        classe.creator = creator

        # Save the updated class object
        classe.save()

        # Show a success message
        messages.success(request, "Class successfully updated.")
        return redirect(reverse('administration:classes'))

    else:
        # If it's a GET request, just render the form
        return render(request, 'administration/editclass.html', {
            "classe": classe,
            "departments": departments
        })
    
    
def delete_class(request,id):
    item=Classe.objects.get(id=id)
    p=item.delete()
    if p:
        messages.warning(request,"You Succesfully deleted the class")
        return redirect(reverse('administration:classes'))
    else:
        messages.warning("Error upon deleting try again")
        return redirect(reverse('administration:classes'))