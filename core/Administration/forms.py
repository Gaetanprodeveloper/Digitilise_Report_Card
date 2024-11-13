from django import forms
from core.models import *

class ClasseForm(forms.ModelForm):
    class Meta:
        model=Classe
        fields='__all__'
        exclude=['creator','creationdate']