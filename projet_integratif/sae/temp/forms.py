from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models

class capteurForm(ModelForm):
    class Meta:
        model = models.capteur
        fields = ('nom',)
        labels = {
            'nom' : _('nom'),
    }

class donneesForm(ModelForm):
    class Meta:
        model = models.donnees
        fields = ('valeur', 'capteur', 'date', 'heure')
        labels = {
            'valeur' : _('valeur'),
            'capteur' : _('capteur'),
            'date' : _('date'),
            'heure': _('heure'),
    }