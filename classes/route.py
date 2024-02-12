import random

from .constantes import *
from .graph import Graph

class Route:

    # Constructeur
    def __init__(self, graph):
        self.graph    = graph
        self.parcours = []
        self.distance_total = -1

    # Méthodes
    def generer_route_aleatoire(self):
        # 1er élément
        self.parcours.append(0)
        # Récupération de la listes des lieux
        lieux_disponibles = self.graph.get_list().copy()
        # Drop du premier lieu
        lieux_disponibles.pop(0)
        # Mélange de la liste des lieux
        random.shuffle(lieux_disponibles)
        # Ajout de la liste mélangée
        self.parcours.extend([int(lieu.getNom()) for lieu in lieux_disponibles])
        # Retour au point de départ
        self.parcours.append(0)
        # Calcul de la distance totale
        self.distance_total = self.calcul_distance_route()

    def generer_route_plus_proche_voisin(self):
        lieu_actuel = self.graph.liste_lieux[0]  # Commencer depuis le premier lieu
        self.ordre.append(int(lieu_actuel.nom))
        lieux_a_visiter = self.graph.liste_lieux.copy()
        lieux_a_visiter.remove(lieu_actuel)

        while lieux_a_visiter:
            plus_proche = self.graph.plus_proche_voisin(lieu_actuel)
            self.ordre.append(int(plus_proche.nom))
            lieux_a_visiter.remove(plus_proche)
            lieu_actuel = plus_proche

        self.ordre.append(0)  # Retour au point de départ

    def calcul_distance_route(self):
        distance_totale = 0
        for i in range(len(self.ordre) - 1):
            distance_totale += self.graph.matrice_od[self.ordre[i]][self.ordre[i + 1]]
        return distance_totale
    def calcul_distance_route(self):
        # Initialisation de la distance
        distance_totale = 0
        # Ajout de chaque arc
        for i in range(len(self.parcours) - 1):
            distance_totale += self.graph.get_distance(self.parcours[i], self.parcours[i + 1])
        # Retourne la distance totale
        return distance_totale

    def __repr__(self):
        output = ''
        for i in range(NB_LIEUX+1):
            output += str(self.parcours[i])
            if i < NB_LIEUX:
                output += ' - '
        output += '\nDistance totale : ' + str(self.distance_total)

        return output