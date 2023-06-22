from django.db import models
from django.conf import settings

class capteur (models.Model):
    nom = models.CharField(max_length=255, unique=True)
    piece = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class donnees(models.Model):
    valeur = models.IntegerField(null = False, blank= False)
    capteur = models.ForeignKey("capteur", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null = False, blank= False)

    def __str__(self):
        return f"Donnée du capteur {self.capteur.nom} ({self.timestamp})"