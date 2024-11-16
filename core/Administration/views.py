from django.shortcuts import get_object_or_404, render,redirect
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
    
@login_required    
def delete_class(request,id):
    item=Classe.objects.get(id=id)
    p=item.delete()
    if p:
        messages.warning(request,"You Succesfully deleted the class")
        return redirect(reverse('administration:classes'))
    else:
        messages.warning("Error upon deleting try again")
        return redirect(reverse('administration:classes'))

@login_required   
def createdepartment(request):
    user=request.user
    if request.method=="POST":
        departmentname=request.POST['departmentname']
        departmentcode=request.POST['departmentcode']
        creator=Administrator.objects.get(user=user)
        department=Department.objects.create(
            creator=creator,
            departmentname=departmentname,
            departmentcode=departmentcode
        )
        if department:
            messages.success(request,'Succesfully created new department')
            return redirect(reverse('administration:managedepartment'))
        else:
            messages.warning(request,'Error try again')
            return redirect(reverse('administration:createdepartment'))
    else:
        return render(request,'administration/add_department.html',{}) 
    
@login_required    
def managedepartments(request):
    departments=Department.objects.all
    return render(request,'administration/managedepartment.html',{"departments":departments}) 

@login_required
def viewdepartment(request,id):
    department=Department.objects.get(id=id)
    return render(request,'administration/viewdepartment.html',{'department':department})  

@login_required
def updatedepartment(request,id):
    department=Department.objects.get(id=id)
    if request.method=="POST":
        departmentname=request.POST['departmentname']
        departmentcode=request.POST['departmentcode']
        department.departmentname=departmentname
        department.departmentcode=departmentcode
        department.save()
        messages.success(request,'Succesfully Updated Department')
        return redirect(reverse('administration:managedepartment'))
    else:    
        return render(request,'administration/updatedepartment.html',{'department':department})
    
    
@login_required
def deletedepartment(request,id):
    department=Department.objects.get(id=id)
    delete=department.delete()
    if delete:
        messages.success(request,'Department Successfully deleted')
        return redirect(reverse('administration:managedepartment'))
    else:
        messages.warning(request,'An error occured try again')
        return redirect(reverse('administration:managedepartment'))

@login_required
def createstudent(request):
    classes = Classe.objects.all()  # Ensure this is called as a function

    if request.method == 'POST':
        # Get form data
        usersname = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        tutoremail = request.POST['tutoremail']
        gender = request.POST['gender']
        classe = request.POST['class']
        dateofbirth = request.POST['dateofbirth']
        address = request.POST['address']
        phone = request.POST['phone']
        pic = request.FILES.get('pic')  # Use .get() to safely get file input

        # Check if username already exists
        if User.objects.filter(username=usersname).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect(reverse('administration:createstudent'))

        # Fetch class and creator
        studentclass = Classe.objects.get(classcode=classe)
        creator = Administrator.objects.get(user=request.user)
        
        # Create student user
        student = User.objects.create_user(username=usersname, password="student")  # You might want to set a default password or prompt for one

        # Set additional fields for the student user
        student.first_name = firstname
        student.last_name = lastname
        student.email = email  # Optionally set the student's email
        student.save()

        # Create the student instance
        studentcreated = Student.objects.create(
            creator=creator,
            user=student,
            usersname=usersname,
            firstname=firstname,
            lastname=lastname,
            email=email,
            parentemail=tutoremail,
            gender=gender,
            classe=studentclass,
            dateofbirth=dateofbirth,
            address=address,
            phonenumber=phone,
            picture=pic
        )

        if studentcreated:
            messages.success(request, 'Student successfully created!')
            return redirect(reverse('administration:studentlist'))
        else:
            messages.warning(request, 'Error occurred. Please try again.')
            return redirect(reverse('administration:createstudent'))

    else:    
        # Render the create student form with available classes
        return render(request, 'administration/createstudent.html', {"classes": classes})
    
    
def studentlist(request):
    students=Student.objects.all()
    return render(request,'administration/studentlist.html',{'students':students})


def student_detail(request, id):
    # Fetch the student using the unique student ID
    student = get_object_or_404(Student, id=id)
    
    return render(request, 'administration/viewstudent.html', {'student': student})


def updatestudent(request, id):
    student = Student.objects.get(id=id)
    classes = Classe.objects.all()  # Ensure this is called as a function

    if request.method == 'POST':
        # Get form data
        usersname = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        tutoremail = request.POST['tutoremail']
        gender = request.POST['gender']
        classe = request.POST['class']
        dateofbirth = request.POST['dateofbirth']
        address = request.POST['address']
        phone = request.POST['phone']
        
        # Handle file upload for picture
        pic = request.FILES.get('pic')  # Use .get() to avoid KeyError if no file is uploaded

        # Update student object fields
        student.firstname = firstname
        student.lastname = lastname
        student.usersname = usersname  # Ensure correct field name
        student.email = email
        student.parentemail = tutoremail
        student.gender = gender
        student.classe = Classe.objects.get(classcode=classe)
        student.dateofbirth = dateofbirth
        student.address = address
        student.phonenumber = phone
        
        # Handle picture upload (if a new picture is uploaded)
        if pic:
            student.picture = pic
        
        # Update associated user model
        user = student.user

        # Check for username uniqueness
        if user.username != usersname:
            try:
                User.objects.get(username=usersname)
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect(reverse('administration:updatestudent', args=[id]))
            except User.DoesNotExist:
                user.username = usersname
        
        # Optionally, you can set a password only if the user provides a new password
        new_password = request.POST.get('password', None)
        if new_password:
            user.set_password(new_password)  # Don't store plain text password
        
        user.save()

        # Save student object
        student.save()

        # Show success message
        messages.success(request, 'Student successfully updated!')
        return redirect(reverse('administration:studentlist'))

    else:
        # Render the update form with the current student's data and classes
        return render(request, 'administration/updatestudent.html', {"student": student, "classes": classes})
    
def deletestudent(request,id):
    student=Student.objects.get(id=id)
    user=student.user
    delete=user.delete()
    if delete:
        messages.warning(request,"Successfully deleted")
    return redirect(reverse('administration:studentlist'))

