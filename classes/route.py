import random

from .constantes import *
from .graph import Graph

class Route:

    # Constructeur
    def __init__(self, graph, parcours=None):
        if parcours != None:
            self.__parcours = parcours.copy()
        else:
            self.generer_route_aleatoire()
        self.__distance_totale = graph.calcul_distance_route(self.__parcours)
    
    # Getters 
    def getParcours(self):
        return self.__parcours
    
    def getDistanceTotale(self):
        return self.__distance_totale

    # Méthodes
    def generer_route_aleatoire(self):
        # 1er élément
        self.__parcours = []
        self.__parcours.append(0)
        # Récupération de la listes des lieux
        lieux_disponibles = [i for i in range(1, NB_LIEUX)]
        # Mélange de la liste des lieux
        random.shuffle(lieux_disponibles)
        # Ajout de la liste mélangée
        self.__parcours.extend([lieu for lieu in lieux_disponibles])
        # Retour au point de départ
        self.__parcours.append(0)

    def generer_route_plus_proche_voisin(self, graph):
        # Ajout du point de départ
        parcours = []
        parcours.append(0)
        lieux_a_visiter = [i for i in range(1, NB_LIEUX)]

        # Création du parcours
        lieu_actuel = 0
        while len(lieux_a_visiter) > 0:
            plus_proche = graph.plus_proche_voisin(lieu_actuel, parcours)
            parcours.append(plus_proche)
            lieux_a_visiter.remove(plus_proche)
            lieu_actuel = plus_proche

        # Retour au point de départ
        parcours.append(0) 
        self.__parcours = parcours

    def __repr__(self):
        output = ''
        for i in range(NB_LIEUX+1):
            output += str(self.__parcours[i])
            if i < NB_LIEUX:
                output += ' - '
        output += '\nDistance totale : ' + str(self.__distance_totale)

        return output