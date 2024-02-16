import random

from .constantes import *
from .graph import Graph

class Route:

    # Constructeur
    def __init__(self, graph, parcours=None, methode='alea', point_depart=0):
        # Initialisation de la route
        if parcours != None:
            self.__parcours = parcours.copy()
        else:
            if methode == 'alea':
                self.generer_route_aleatoire()
            else:
                self.generer_route_plus_proche_voisin(graph, point_depart)

        # Calcul de la distance totale
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

    def generer_route_plus_proche_voisin(self, graph, lieu_depart=0):
        # Ajout du point de départ
        parcours = []
        parcours.append(0)
        lieux_a_visiter = [i for i in range(1, NB_LIEUX)]

        # Création du parcours
        if lieu_depart != 0: 
            parcours.append(lieu_depart)
            lieux_a_visiter.remove(lieu_depart)
        lieu_actuel = lieu_depart
        while len(lieux_a_visiter) > 0:
            plus_proche = graph.plus_proche_voisin(lieu_actuel, parcours)
            parcours.append(plus_proche)
            lieux_a_visiter.remove(plus_proche)
            lieu_actuel = plus_proche

        # Retour au point de départ
        parcours.append(0) 
        self.__parcours = parcours

    # Setters
    def swap(self, indice_un, indice_deux):
        # Effectue un swap entre deux élèments
        temp = self.__parcours[indice_un]
        self.__parcours[indice_un]   = self.__parcours[indice_deux]
        self.__parcours[indice_deux] = temp
    
    def set_distance_totale(self, nouvelle_distance):
        self.__distance_totale = nouvelle_distance

    # Opérateurs 
    def __repr__(self):
        output = ''
        for i in range(NB_LIEUX+1):
            output += str(self.__parcours[i])
            if i < NB_LIEUX:
                output += ' - '
        output += '\nDistance totale : ' + str(self.__distance_totale)

        return output