from django.contrib import admin

from .models import *


tables=[Administrator,Classe,Lecturer,Student,Course,Mark,Department]

admin.site.register(tables)
# Register your models here.
