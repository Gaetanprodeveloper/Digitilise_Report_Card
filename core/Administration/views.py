from datetime import datetime
import io
import zipfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.urls import reverse
from core.models import *
from core.Administration import forms
from django.contrib.auth.decorators import login_required
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
from pdfkit.configuration import Configuration
from xhtml2pdf import pisa


@login_required
def home(request):
    user=request.user
    
    users=User.objects.count()
    administrators=Administrator.objects.count()
    students=Student.objects.count()
    lecturers=Lecturer.objects.count()
    courses=Course.objects.count()
    classes=Classe.objects.count()
    departments=Department.objects.count()
    
    
    return render(request,'Administration/home.html',
                  {"user":user,
                   "users":users,
                   "administrators":administrators,
                   "students":students,
                   "lecturers":lecturers,
                   "courses":courses,
                   "classes":classes,
                   "departments":departments 
                   })

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
        
        if Department.objects.filter(departmentname=departmentname).exists():
            messages.warning(request,"Department already exist")
            return redirect(reverse('administration:createdepartment'))
        
            
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
    
@login_required    
def studentlist(request):
    students=Student.objects.all()
    return render(request,'administration/studentlist.html',{'students':students})


@login_required
def student_detail(request, id):
    # Fetch the student using the unique student ID
    student = get_object_or_404(Student, id=id)
    
    return render(request, 'administration/viewstudent.html', {'student': student})


@login_required
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

@login_required    
def deletestudent(request,id):
    student=Student.objects.get(id=id)
    user=student.user
    delete=user.delete()
    if delete:
        messages.success(request,"Successfully deleted")
    return redirect(reverse('administration:studentlist'))


@login_required
def createlecturers(request):
    user = request.user
    departments = Department.objects.all()
    if request.method == "POST":
        usersname = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        department_name = request.POST['department']
        dateofbirth = request.POST['dateofbirth']
        address = request.POST['address']
        phonenumber = request.POST['phonenumber']
        picture = request.FILES['picture']
        email = request.POST['email']
        
        # Check if username exists
        if User.objects.filter(username=usersname).exists():
            messages.warning(request, 'Username already exists. Please choose another username.')
            return redirect(reverse('administration:createlecturer'))

        creator = Administrator.objects.get(user=user)
        department = Department.objects.get(departmentname=department_name)
        new_user = User.objects.create_user(username=usersname, password="lecturer")
        
        new_user.first_name=firstname
        new_user.last_name=lastname
        new_user.save()

        if new_user:
            lecturer = Lecturer.objects.create(
                creator=creator,
                user=new_user,
                department=department,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                dateofbirth=dateofbirth,
                address=address,
                email=email,
                phonenumber=phonenumber,
                picture=picture
            )
            if lecturer:
                messages.success(request, 'Lecturer successfully created.')
                return redirect(reverse('administration:managelecturer'))
            else:
                messages.warning(request, 'Error, try again.')
                return redirect(reverse('administration:createlecturer'))
    return render(request, 'administration/addlecturer.html', {'departments': departments})

@login_required
def managelecturer(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'administration/managelecturer.html', {'lecturers': lecturers})



@login_required
def lecturer_detail(request, id):
    # Fetch the lecturer using the unique lecturer ID
    lecturer = get_object_or_404(Lecturer, id=id)
    
    return render(request, 'administration/viewlecturer.html', {'lecturer': lecturer})



@login_required
def updatelecturer(request, id):
    lecturer = Lecturer.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        # Get form data
        usersname = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        department_name = request.POST['department']
        dateofbirth = request.POST['dateofbirth']
        address = request.POST['address']
        phone = request.POST['phone']

        # Handle file upload for picture
        pic = request.FILES.get('pic')  # Use .get() to avoid KeyError if no file is uploaded

        # Update lecturer object fields
        lecturer.firstname = firstname
        lecturer.lastname = lastname
        lecturer.email = email
        lecturer.gender = gender
        lecturer.department = Department.objects.get(departmentname=department_name)
        lecturer.dateofbirth = dateofbirth
        lecturer.address = address
        lecturer.phonenumber = phone

        # Handle picture upload (if a new picture is uploaded)
        if pic:
            lecturer.picture = pic

        # Update associated user model
        user = lecturer.user

        # Check for username uniqueness
        if user.username != usersname:
            try:
                User.objects.get(username=usersname)
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect(reverse('administration:updatelecturer', args=[id]))
            except User.DoesNotExist:
                user.username = usersname

        # Optionally, you can set a password only if the user provides a new password
        new_password = request.POST.get('password', None)
        if new_password:
            user.set_password(new_password)  # Don't store plain text password

        user.save()

        # Save lecturer object
        lecturer.save()

        # Show success message
        messages.success(request, 'Lecturer successfully updated!')
        return redirect(reverse('administration:managelecturer'))

    else:
        # Render the update form with the current lecturer's data and departments
        return render(request, 'administration/updatelecturer.html', {"lecturer": lecturer, "departments": departments})
    
    
    
@login_required    
def deletelecturer(request,id):
    lecturer=Lecturer.objects.get(id=id)
    user=lecturer.user
    delete=user.delete()
    if delete:
        messages.success(request,"Successfully deleted")
    return redirect(reverse('administration:managelecturer'))


@login_required
def create_course(request):
    # Fetch the existing lecturers and classes for the dropdown options
    lecturers = Lecturer.objects.all()
    classes = Classe.objects.all()
    
    if request.method == 'POST':
        # Get current logged in user (administrator)
        user = request.user
        creator = Administrator.objects.get(user=user)
        
        # Collect data from the form
        title = request.POST['coursetitle']
        code = request.POST['coursecode']
        credits = request.POST['credits']
        semester = request.POST['semester']
        classe_name = request.POST['class']
        lecturer_name = request.POST['lecturer']
        
        # Fetch the class and lecturer objects based on their names
        classe = Classe.objects.get(classcode=classe_name)
        lecturer = Lecturer.objects.get(firstname=lecturer_name)
        
        # Create the course
        course = Course.objects.create(
            creator=creator,
            lecturer=lecturer,
            classe=classe,
            coursecode=code,
            coursetitle=title,
            credits=credits,
            semester=semester,
        )
        
        # Check if the course was created and send a message
        if course:
            messages.success(request, "Course created successfully!")
            return redirect('administration:managecourse')  # Redirect to the list of courses
        else:
            messages.error(request, "Error creating the course.")
            return redirect(reverse('administration:createcourse'))  # Stay on the create course page
    
    else:
        # Return to the form page if the method is GET
        return render(request, 'administration/createcourse.html', {
            'lecturers': lecturers,
            'classes': classes,
            'semesters': Course.SEMESTER  # Pass the SEMESTER choices to the template
        })
        

@login_required       
def managecourse(request):
    # Get all courses created by the current administrator
    courses = Course.objects.all()
    return render(request,'administration/managecourse.html',{'courses':courses})


@login_required 
def viewcourse(request, id):
    # Get the course object or return a 404 if not found
    course = get_object_or_404(Course, id=id)
    
    # Render the course details page
    return render(request, 'Administration/viewcourse.html', {'course': course})

@login_required 
def updatecourse(request, id):
    # Get the course object or return a 404 if not found
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        # Update course details from the form
        course.coursetitle = request.POST['coursetitle']
        course.coursecode = request.POST['coursecode']
        course.credits = request.POST['credits']
        course.semester = request.POST['semester']
        
        # Update related foreign key objects
        classe_name = request.POST['class']
        lecturer_name = request.POST['lecturer']
        course.classe = Classe.objects.get(classcode=classe_name)
        course.lecturer = Lecturer.objects.get(firstname=lecturer_name)
        
        # Save the updated course
        course.save()
        messages.success(request, 'Course updated successfully')
        return redirect('administration:managecourse')

    # Get all classes and lecturers for the form dropdowns
    classes = Classe.objects.all()
    lecturers = Lecturer.objects.all()

    return render(request, 'Administration/updatecourse.html', {
        'course': course,
        'classes': classes,
        'lecturers': lecturers,
        'semesters': Course.SEMESTER
    })
    
    
def deletecourse(request,id):
    course=Course.objects.get(id=id)
    delete=course.delete()
    if delete:
        messages.success(request,'Course deleted successfully')
        return redirect('administration:managecourse')
    return render(request)


@login_required
def get_course_semester(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        return JsonResponse({
            'semester': course.semester,
            'lecturer': f"{course.lecturer.firstname} {course.lecturer.lastname}",
            'lecturer_id': course.lecturer.id,
            'lecturer_name': course.lecturer.firstname + ' ' + course.lecturer.lastname,
            
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)  # Assuming `semester` is a field in the `Course` model.

@login_required
def createmark(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        lecturer_id = request.POST.get('lecturer')
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        mark = request.POST.get('mark')
        grade = request.POST.get('grade')
        
         # Ensure that lecturer_id is an integer
        try:
            lecturer_id = int(lecturer_id)  # Convert to integer to prevent any string errors
        except ValueError:
            messages.error(request, "Invalid lecturer ID.")
            return redirect('administration:marks')

        student = get_object_or_404(Student, id=student_id)
        lecturer = get_object_or_404(Lecturer, id=lecturer_id)
        course = get_object_or_404(Course, id=course_id)
        user = request.user
        creator = Administrator.objects.get(user=user)

        existing_mark = Mark.objects.filter(student=student, course=course, semester=semester).first()

        if existing_mark:
            messages.error(request, 'This student already has a mark for this course and semester.')
            return redirect('administration:marks')

        try:
            mark = int(mark)
            if not (0 <= mark <= 20):
                raise ValueError("Mark must be between 0 and 20.")
        except ValueError as e:
            messages.error(request, f"Invalid input for mark: {e}")
            return redirect('administration:createmark')

        new_mark = Mark.objects.create(
            creator=creator,
            student=student,
            lecturer=lecturer,
            course=course,
            mark=mark,
            grade=grade,
            semester=semester,
        )
        new_mark.save()
        messages.success(request, 'Mark created successfully')
        return redirect('administration:managemarks')

    students = Student.objects.all()
    #lecturers = Lecturer.objects.all()
    courses = Course.objects.all()
    grades = Mark.Grade

    return render(request, 'Administration/createmark.html', {
        'students': students,
        'courses': courses,
        'grades': grades,
    })
    
@login_required   
def managemarks(request):
    marks=Mark.objects.all()
    return render(request, 'Administration/managemarks.html',{'marks':marks})


@login_required
def updatemark(request, id):
    # Get the mark object or return a 404 if not found
    mark = get_object_or_404(Mark, id=id)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        lecturer_id = request.POST.get('lecturer')
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        mark_value = request.POST.get('mark')
        grade = request.POST.get('grade')

        # Ensure that lecturer_id is an integer
        try:
            lecturer_id = int(lecturer_id)  # Convert to integer to prevent any string errors
        except ValueError:
            messages.error(request, "Invalid lecturer ID.")
            return redirect('administration:updatemark', id=id)

        student = get_object_or_404(Student, id=student_id)
        lecturer = get_object_or_404(Lecturer, id=lecturer_id)
        course = get_object_or_404(Course, id=course_id)
        user = request.user
        creator = Administrator.objects.get(user=user)

        # Check if the student already has a mark for this course and semester
        if mark.student != student or mark.course != course or mark.semester != semester:
            existing_mark = Mark.objects.filter(student=student, course=course, semester=semester).first()
            if existing_mark and existing_mark.id != mark.id:
                messages.error(request, 'This student already has a mark for this course and semester.')
                return redirect('administration:updatemark', id=id)

        try:
            mark_value = int(mark_value)
            if not (0 <= mark_value <= 20):
                raise ValueError("Mark must be between 0 and 20.")
        except ValueError as e:
            messages.error(request, f"Invalid input for mark: {e}")
            return redirect('administration:updatemark', id=id)

        # Update the mark record
        mark.creator = creator
        mark.student = student
        mark.lecturer = lecturer
        mark.course = course
        mark.mark = mark_value
        mark.grade = grade
        mark.semester = semester
        mark.save()

        messages.success(request, 'Mark updated successfully')
        return redirect('administration:managemarks')

    # Pass data to the template for rendering
    students = Student.objects.all()
    lecturers = Lecturer.objects.all()
    courses = Course.objects.all()
    grades = Mark.Grade

    return render(request, 'Administration/updatemark.html', {
        'mark': mark,
        'students': students,
        'lecturers': lecturers,
        'courses': courses,
        'grades': grades,
    })

def viewmark(request,id):
    mark = get_object_or_404(Mark, id=id)
    return render(request, 'Administration/viewmark.html', {'mark': mark})

def deletemark(request,id):
    mark=Mark.objects.get(id=id)
    delete=mark.delete()
    if delete:
        messages.success(request,'mark deleted successfully')
        return redirect('administration:managemarks')
    return render(request)



def select_class_semester_report(request):
    classes = Classe.objects.all()
    semesters = Course.SEMESTER  # Assuming the semesters are stored as tuples
    
    if request.method == "POST":
        class_id = request.POST.get('class_choices')
        semester = request.POST.get('semester_choices')
        return generate_class_report_cards(request, class_id, semester)
    
    return render(
        request,
        "Administration/select_class_semester_report.html",
        {
            "classes": classes,
            "semesters": semesters,
        },
    )

def generate_class_report_cards(request, class_id, semester):
    # Get the class and students
    selected_class = Classe.objects.get(id=class_id)
    students = Student.objects.filter(classe=selected_class)
    academic_year = f"{datetime.now().year - 1}/{datetime.now().year}"

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for student in students:
            # Prepare student-specific data
            marks = Mark.objects.filter(student=student, semester=semester)
            total_marks = sum(mark.mark * mark.course.credits for mark in marks)
            total_credits = sum(mark.course.credits for mark in marks)
            average = total_marks / total_credits if total_credits else 0

            # Render HTML for the student's report
            html_content = render_to_string(
                "Administration/class_report_template.html",
                {
                    "student": student,
                    "marks": marks,
                    "average": average,
                    "class_name": selected_class.classname,
                    "semester": semester,
                    'academic_year':academic_year,
                    "current_date": datetime.now().strftime("%d/%m/%Y"),
                },
            )

            # Generate PDF
            pdf_buffer = io.BytesIO()
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
            if pisa_status.err:
                return HttpResponse(f"An error occurred while generating PDF for {student.firstname} {student.lastname}.")

            # Add PDF to ZIP file
            pdf_buffer.seek(0)
            zip_file.writestr(f"{student.firstname}_{student.lastname}_report.pdf", pdf_buffer.read())

    # Send ZIP file as response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="class_reports_{selected_class.classname}_{semester}.zip"'
    return response
