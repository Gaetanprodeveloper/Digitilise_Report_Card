from django.db import models
from django.contrib.auth.models import User

class Administrator(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    gender=models.CharField(max_length=1)
    creationdate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lastname
    
class Classe(models.Model):
    creator=models.ForeignKey(Administrator,on_delete=models.DO_NOTHING)
    classcode=models.CharField(max_length=10)
    classname=models.CharField(max_length=255)
    level=models.IntegerField()
    speciality=models.CharField(max_length=255)
    creationdate=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.classname
    
class Department(models.Model):
    creator=models.ForeignKey(Administrator,on_delete=models.DO_NOTHING)
    departmentcode=models.CharField(max_length=20)
    departmentname=models.CharField(max_length=255)

    def __str__(self):
        return self.departmentname
    
class Student(models.Model):
    creator=models.ForeignKey(Administrator,on_delete=models.DO_NOTHING)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    usersname=models.CharField(max_length=255)
    gender=models.CharField(max_length=1)
    dateofbirth=models.DateField()
    address=models.CharField(max_length=200,default='Bepanda')
    phonenumber=models.CharField(max_length=20,default='+237677285763')
    picture=models.ImageField(null=False,upload_to='students/',default='teacher.png')
    parentemail=models.EmailField()
    creationdate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstname
    
class Lecturer(models.Model):
    creator=models.ForeignKey(Administrator,on_delete=models.DO_NOTHING)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    gender=models.CharField(max_length=1)
    dateofbirth=models.DateField()
    email=models.EmailField()
    creationdate=models.DateTimeField(auto_now=True)
    address=models.CharField(max_length=200,default='Logbaba')
    phonenumber=models.IntegerField(default=677285764)
    picture=models.ImageField(null=False,upload_to='lecturer_pictures',default='teacher.png')
    def __str__(self):
        return self.firstname
    

class Course(models.Model):
    
    SEMESTER_1='semester 1'
    SEMESTER_2='semester 2'
    SEMESTER_3='semester 3'
    SEMESTER_4='semester 4'
    SEMESTER_5='semester 5'
    SEMESTER_6='semester 6'
    SEMESTER_7='semester 7'
    SEMESTER_8='semester 8'
    SEMESTER_9='semester 9'
    SEMESTER_10='semester 10'
    SEMESTER_11='semester 11'
    SEMESTER_12='semester 12'
    SEMESTER_13='semester 13'
    SEMESTER_14='semester 14'
    SEMESTER=(
        (SEMESTER_1,'semester 1'),(SEMESTER_2,'semester 2'),(SEMESTER_3,'semester 3'),(SEMESTER_4,'semester 4'),
        (SEMESTER_5,'semester 5'),(SEMESTER_6,'semester 6'),(SEMESTER_7,'semester 7'),(SEMESTER_8,'semester 8'),
        (SEMESTER_9,'semester 9'),(SEMESTER_10,'semester 10'),(SEMESTER_11,'semester 11'),(SEMESTER_12,'semester 12'),
        (SEMESTER_13,'semester 13'),(SEMESTER_14,'semester 14')
    )
    
    creator=models.ForeignKey(Administrator,on_delete=models.CASCADE)
    lecturer=models.ForeignKey(Lecturer,on_delete=models.CASCADE)
    classe=models.ForeignKey(Classe,on_delete=models.CASCADE)
    coursecode=models.CharField(max_length=10)
    coursetitle=models.CharField(max_length=255)
    credits=models.IntegerField()
    semester=models.CharField(max_length=25,choices=SEMESTER,default=SEMESTER_1)
    creationdate=models.DateField(auto_now=True)

    def __str__(self):
        return self.coursetitle 
    
    
class Mark(models.Model):
    
    Grade_A1="A+"
    Grade_A2="A"
    Grade_A3="A-"
    Grade_B1="B+"
    Grade_B2="B"
    Grade_B3="B-"
    Grade_C1="C+"
    Grade_C2="C"
    Grade_C3="C-"
    Grade_D="D"
    Grade_E="E"
    Grade_F="F"
    
    Grade=(
        (Grade_A1,"A+"),(Grade_A2,"A"),(Grade_A3,"A-"),
        (Grade_B1,"B+"),(Grade_B2,"B"),(Grade_B3,"B-"),
        (Grade_C1,"C+"),(Grade_C2,"C"),(Grade_C3,"C-"),
        (Grade_D,"D"),(Grade_E,"E"),(Grade_F,"F"),
    )
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    lecturer=models.ForeignKey(Lecturer,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    mark=models.IntegerField()
    grade=models.CharField(max_length=10,choices=Grade,default=Grade_A1)
    semester=models.CharField(max_length=25)



# Create your models here.
