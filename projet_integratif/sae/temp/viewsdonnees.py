from django.shortcuts import render
from .forms import donneesForm
from . import models
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os

def affiche(request):
    base = list(models.donnees.objects.all())
    return render(request, "temp/donnees/affiche.html", {"base": base})


def affiche1(request, id):
    base = list(models.capteur.objects.filter(capteur=id))
    return render(request, "temp/capteur/affiche0.html", {"base": base})
