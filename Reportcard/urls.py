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
from django.contrib import admin
from django.urls import path,include
from core import views
from core.Administration import views as views_administration
from core.Lecturer import views as views_lecturer
from core.Student import views as views_student
from django.contrib.auth import views as auth_views

administrator_urlpatters=[
    path('',views_administration.home, name='home'),
    path('createclass/',views_administration.createclass, name='createclass'),
    path('classes/',views_administration.classes, name='classes'),
    path('classes/<id>/',views_administration.moreinfoclass, name='classeinfo'),
    path('classes/update/<id>/',views_administration.updateclass, name='updateclass'),
    path('classes/delete/<id>/',views_administration.delete_class, name='deleteclass')
    
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
