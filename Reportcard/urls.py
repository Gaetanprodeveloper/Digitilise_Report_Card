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
from core.Administration import views as viws_administration
from core.Lecturer import views as views_lecturer
from core.Student import views as views_student

administrator_urlpatters=[
    
]

lecturer_urlpatters=[
    
]

student_urlpatters=[
    
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_page,name='login'),
    path('administration/',include((administrator_urlpatters,'administration'))),
    path('lecturer',include((lecturer_urlpatters, 'lecturer'))),
    path('student',include((student_urlpatters, 'student')))
]
