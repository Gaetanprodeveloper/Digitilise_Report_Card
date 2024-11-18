"""
URL configuration for Reportcard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from core import views
from core.Administration import views as views_administration
from core.Lecturer import views as views_lecturer
from core.Student import views as views_student
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

administrator_urlpatters=[
    path('',views_administration.home, name='home'),
    path('createclass/',views_administration.createclass, name='createclass'),
    path('classes/',views_administration.classes, name='classes'),
    path('classes/<id>/',views_administration.moreinfoclass, name='classeinfo'),
    path('classes/update/<id>/',views_administration.updateclass, name='updateclass'),
    path('classes/delete/<id>/',views_administration.delete_class, name='deleteclass'),
    path('createdepartment/',views_administration.createdepartment, name='createdepartment'),
    path('managedepartment/',views_administration.managedepartments, name='managedepartment'),
    path('departments/<id>/',views_administration.viewdepartment, name='viewdepartment'),
    path('department/update/<id>/',views_administration.updatedepartment, name='updatedepartment'),
    path('department/delete/<id>/',views_administration.deletedepartment, name='deletedepartment'),
    path('createstudent/',views_administration.createstudent, name='createstudent'),
    path('students/',views_administration.studentlist, name='studentlist'),
    path('student/<id>/',views_administration.student_detail, name='viewstudent'),
    path('student/update/<id>/',views_administration.updatestudent, name='updatestudent'),
    path('student/delete/<id>/',views_administration.deletestudent, name='deletestudent'),
    path('createlecturer/',views_administration.createlecturers, name='createlecturer'),
    path('lecturers/',views_administration.managelecturer, name='managelecturer'),
    path('lecturer/<id>/',views_administration.lecturer_detail, name='lecturerdetail'),
    path('lecturer/update/<id>/',views_administration.updatelecturer, name='updatelecturer'),
    path('lecturer/delete/<id>/',views_administration.deletelecturer, name='deletelecturer'),
    path('createcourse/',views_administration.create_course, name='createcourse'),
    path('courses/',views_administration.managecourse, name='managecourse'),
    path('courses/<id>/',views_administration.viewcourse, name='viewcourse'),
    path('courses/<id>/update/',views_administration.updatecourse, name='updatecourse'),
    path('courses/<id>/delete/',views_administration.deletecourse, name='deletecourse'),
    path('createmark/',views_administration.createmark, name='marks'),
    path('marks/',views_administration.managemarks, name='managemarks'),
    path('get-semester/<int:course_id>/', views_administration.get_course_semester, name='get_course_semester'),
    path('marks/update/<id>/',views_administration.updatemark, name='updatemark'),
    path('marks/<id>/',views_administration.viewmark, name='viewmark'),
    path('marks/delete/<id>/',views_administration.deletemark, name='deletemark'),
    
]

lecturer_urlpatters=[
    path('',views_lecturer.home, name='home')
    
]

student_urlpatters=[
    path('',views_student.home, name='home')
    
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_page,name='login'),
    path('sign-out/',auth_views.LogoutView.as_view(next_page="login"), name='sign-out'),
    path('administration/',include((administrator_urlpatters,'administration'))),
    path('lecturer',include((lecturer_urlpatters, 'lecturer'))),
    path('student',include((student_urlpatters, 'student')))
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)