from django import forms
from .models import Donnee, Capteur

class DonneeForm(forms.ModelForm):
    class Meta:
        model = Donnee
        fields = ['capteur', 'date', 'heure', 'temperature']

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = ['piece']
