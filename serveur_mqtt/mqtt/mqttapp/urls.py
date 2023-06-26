from django.urls import path
from . import views

app_name = 'mqttapp'

urlpatterns = [
    path('', views.donnees_en_temps_reel, name='donnees_en_temps_reel'),
    path('actualiser-donnees/', views.actualiser_donnees, name='actualiser_donnees'),
    path('filtrer-donnees/', views.filtrer_donnees, name='filtrer_donnees'),
    path('exporter-donnees/', views.exporter_donnees, name='exporter_donnees'),
    path('graph/', views.graph_view, name='graph'),
    path('capteurs/update/<str:pk>/', views.update_piece, name='update_piece'),


]


