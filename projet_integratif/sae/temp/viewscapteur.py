from django.shortcuts import render
from .forms import capteurForm
from . import models
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import os

def affiche(request):
    base = list(models.capteur.objects.all())
    return render(request, "temp/capteur/affiche.html", {"base": base})

def update(request, id):
    form = capteurForm()
    return render(request, "temp/capteur/update.html", {"form": form, "id": id})

def traitement(request, id):
    form = capteurForm(request.POST)
    if form.is_valid():
        form.save(update_fields=['nom'])
        return HttpResponseRedirect("/")
    else:
        return render(request, "temp/capteur/update.html", {"form": form, "id": id})
