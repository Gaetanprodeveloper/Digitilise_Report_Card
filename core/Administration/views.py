from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from core.models import *
from core.Administration import forms



def home(request):
    user=request.user
    return render(request,'Administration/home.html',{"user":user})


def createclass(request):
    if request.method=="POST":
        user=request.user
        speciality=request.POST["speciality"]
        classname=request.POST['classname']
        classcode=request.POST['classcode']
        level=request.POST['level']
        creator=Administrator.objects.get(user=user)
        
        
        classe=Classe.objects.create(
            creator=creator,
            classcode=classcode,
            classname=classname,
            level=level,
            speciality=speciality
            )
        if classe:
            messages.success(request,'Class is added succesfully')
            return redirect(reverse('administration:classes'))
        else:
            messages.warning(request,"Error While creating try again")
            return redirect('createclass')
    else:    
        return render(request,'administration/add_class.html',{})   
    
    
def classes(request):
    classe=Classe.objects.all
    return render(request,'administration/manageclass.html',{"classe":classe})

def moreinfoclass(request,id):
    classe=Classe.objects.get(id=id)
    return render(request,'administration/viewclass.html',{"classe":classe})

def updateclass(request,id):
    classe=Classe.objects.get(id=id)
    if request.method=='POST':
        form=forms.ClasseForm(request.POST,instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request,'Succesfully Updated')
            return redirect(reverse('administration:classes'))
        else:
            messages.warning(request,'An error occured Try again')
    else:        
        return render(request,'administration/editclass.html',{"classe":classe})
    
    
def delete_class(request,id):
    item=Classe.objects.get(id=id)
    p=item.delete()
    if p:
        messages.warning(request,"You Succesfully deleted the class")
        return redirect(reverse('administration:classes'))
    else:
        messages.warning("Error upon deleting try again")
        return redirect(reverse('administration:classes'))