import plotly
from django.http import JsonResponse
from datetime import datetime

def donnees_en_temps_reel(request):
    donnees = Donnee.objects.order_by('-date', '-heure')[:8][::-1]
    capteurs = Capteur.objects.all()
    return render(request, 'mqtt/donnees_en_temps_reel.html', {'donnees': donnees,'capteurs':capteurs})


def actualiser_donnees(request):

    donnees = Donnee.objects.order_by(F('date').desc(), F('heure').desc())[:10]
    serialized_data = []
    for donnee in donnees:
        serialized_data.append({
            'date': donnee.date.strftime('%Y-%m-%d'),
            'heure': donnee.heure.strftime('%H:%M:%S'),
            'temperature': donnee.temperature
        })

    return JsonResponse({'donnees': serialized_data})




def filtrer_donnees(request):
    nom_capteur = request.GET.get('nom-capteur')
    date_debut = request.GET.get('date-debut')
    date_fin = request.GET.get('date-fin')

    donnees = Donnee.objects.all()

    # Filtrer par nom de capteur
    if nom_capteur:
        donnees = donnees.filter(capteur__nom=nom_capteur)

    # Filtrer par date de début et de fin
    if date_debut and date_fin:
        date_debut = datetime.strptime(date_debut, '%d/%m/%Y')
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')
        donnees = donnees.filter(capteur__nom=nom_capteur, date__range=[date_debut, date_fin])
    elif date_debut:
        date_debut = datetime.strptime(date_debut, '%d/%m/%Y')
        donnees = donnees.filter(capteur__nom=nom_capteur, date__gte=date_debut)
    elif date_fin:
        date_fin = datetime.strptime(date_fin, '%d/%m/%Y')
        donnees = donnees.filter(capteur__nom=nom_capteur, date__lte=date_fin)

    donnees = donnees.order_by('-date', '-heure')
    context = {
        'donnees': donnees
    }
    return render(request, 'mqtt/filtrer_donnees.html', context)





import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Donnee, Capteur

import csv
from django.http import HttpResponse
from django.db.models import F

def exporter_donnees(request):
    donnees = Donnee.objects.order_by(F('date').desc(), F('heure').desc())

    # Créer une réponse HTTP avec le type de contenu CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donnees.csv"'

    # Créer un objet CSVWriter
    writer = csv.writer(response)

    # Écrire les en-têtes de colonne dans le fichier CSV
    writer.writerow(['Capteur', 'Date', 'Heure', 'Température'])

    # Écrire les données dans le fichier CSV
    for donnee in donnees:
        writer.writerow([donnee.capteur.nom, donnee.date.strftime('%Y-%m-%d'), donnee.heure.strftime('%H:%M:%S'), donnee.temperature])

    return response

from django.shortcuts import render
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from .models import Donnee

# Créer une application Dash
app = DjangoDash('GraphApp')

# Définir la fonction de vue
from django.shortcuts import render
import plotly.graph_objects as go

from django.shortcuts import render
import plotly.graph_objects as go

def graph_view(request):
    # Récupérer les 10 dernières données de température depuis le modèle Donnee
    donnees = Donnee.objects.order_by('-date', '-heure')[:50]

    # Traiter les données et les préparer pour le graphique
    x_values = [donnees[i].heure for i in range(len(donnees))]
    y_values = [donnees[i].temperature for i in range(len(donnees))]

    # Créer la figure du graphique Plotly
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='lines', name='Temperature'))
    fig.update_layout(title='Graphique des 50 dernières données de température', xaxis_title='Heure', yaxis_title='Température')

    # Convertir la figure en div HTML
    graph_div = fig.to_html(full_html=False, default_height=700, default_width=1000)

    # Passer le div du graphique au template
    context = {'graph_div': graph_div}

    # Rendre le template contenant le graphique
    return render(request, 'mqtt/graph.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Capteur
from .forms import CapteurForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Capteur
from .forms import CapteurForm

def update_piece(request, pk):
    capteur = get_object_or_404(Capteur, pk=pk)

    if request.method == 'POST':
        form = CapteurForm(request.POST, instance=capteur)
        if form.is_valid():
            form.save()
            return redirect('/')  # Rediriger vers la page d'accueil après la modification
    else:
        form = CapteurForm(initial={'piece': capteur.piece})

    context = {'form': form, 'nom_capteur': capteur.nom}
    return render(request, 'mqtt/update_piece.html', context)




