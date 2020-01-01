from .models import *
from django import forms

class CardForm(forms.ModelForm):
    
    class Meta:
        model = Card
        fields = ("txt",)
