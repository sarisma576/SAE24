from django.shortcuts import render
from .forms import donneesForm
from . import models
from .models import capteur, donnees
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os

def affiche(request):
    base = list(models.donnees.objects.all())
    return render(request, "temp/donnees/affiche.html", {"base": base})


def affiche1(request, id):
    base = list(models.capteur.objects.filter(capteur=id))
    return render(request, "temp/capteur/affiche0.html", {"base": base})

def filtrer_capteurs(request):
    # Récupération des paramètres du formulaire
    nom_capteur = request.GET.get('nom', '')
    id_capteur = request.GET.get('id', '')
    date_min_capteur = request.GET.get('date_min', '')
    date_max_capteur = request.GET.get('date_max', '')

    # Filtrage des capteurs en fonction des paramètres
    capteurs = capteur.objects.all()
    if nom_capteur:
        capteurs = capteurs.filter(nom__icontains=nom_capteur)
    if id_capteur:
        capteurs = capteurs.filter(id=id_capteur)

    # Filtrage des données en fonction des paramètres
    donnees_capteurs = donnees.objects.all()
    if date_min_capteur:
        donnees_capteurs = donnees_capteurs.filter(timestamp__gte=date_min_capteur)
    if date_max_capteur:
        donnees_capteurs = donnees_capteurs.filter(timestamp__lte=date_max_capteur)

    context = {
        'capteurs': capteurs,
        'donnees_capteurs': donnees_capteurs,
        'nom_capteur': nom_capteur,
        'id_capteur': id_capteur,
        'date_min_capteur': date_min_capteur,
        'date_max_capteur': date_max_capteur,
    }

    return render(request, 'filtre_capteurs.html', context)

def go (request):
    return render(request, 'temp/test.html')