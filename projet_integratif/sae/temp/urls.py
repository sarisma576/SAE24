from django.urls import path
from . import views,viewscapteur,viewsdonnees

urlpatterns = [
    path('', views.index),

    path('affiche-capteur/', viewscapteur.affiche),
    path('affiche-donnees/', viewsdonnees.affiche),
    path('affiche-donnees/<int:id>', viewsdonnees.affiche1),
    path('update/<int:id>/', viewscapteur.update),
    path('traitement-update/<int:id>/', viewscapteur.traitement),

]