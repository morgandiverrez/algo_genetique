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