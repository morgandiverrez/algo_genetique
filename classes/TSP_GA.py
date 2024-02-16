import random 

from .constantes import *
from .route import Route
from .graph import Graph

def croisement(parent_un, parent_deux):
        # Récupération des parcours des parents
        parcours_parent_un   = parent_un.getParcours()
        parcours_parent_deux = parent_deux.getParcours()
        # Tirage des coupures 
        coupure_un   = 0
        coupure_deux = 0
        while coupure_un >= coupure_deux:
            coupure_un   = random.randint(1, NB_LIEUX)
            coupure_deux = random.randint(1, NB_LIEUX)
        # Création de l'enfant
        parcours_enfant = [-1]*(NB_LIEUX+1)
        parcours_enfant[0] = 0
        parcours_enfant[NB_LIEUX] = 0
        # Copie des données entre les deux coupures 
        for idx in range(coupure_un, coupure_deux+1):
            parcours_enfant[idx] = parcours_parent_un[idx]
        # Copie du reste des données 
        indice = 1
        for idx in range(1, NB_LIEUX+1):
            if idx < coupure_un or idx > coupure_deux:
                while (parcours_parent_deux[indice] in parcours_enfant) and (indice < NB_LIEUX): indice += 1
                parcours_enfant[idx] = parcours_parent_deux[indice]
        
        return parcours_enfant

class TSP_GA:
    # Constructeur
    def __init__(self, graph, taille_pop, proba_mut, proba_crois, part_alea=0.25):
        # Copie du Graph dans un attribut
        self.__g = graph

        # Copie des valeurs de paramètres
        self.__taille_pop  = taille_pop
        self.__proba_mut   = proba_mut
        self.__proba_crois = proba_crois
        self.__part_alea   = part_alea

        # Initialisation de la population
        self.__pop = []
        self.initialisation_population()
        
    # Getters 
    def get_meilleure_route(self):
        return self.__meilleure_route
    
    def get_distance_meilleure_route(self):
        return self.__distance_meilleure_route

    # Méthodes 
    def initialisation_population(self):
        # Création d'une à partir de la méthode gloutonne
        r1 = Route(self.__g, methode='glouton')    
        self.__pop.append(r1)             
        # Garde en mémoire la meilleure route     
        self.__meilleure_route = r1                 
        self.__distance_meilleure_route = r1.getDistanceTotale()
        # Création des autres routes
        points_depart_possibles = [i for i in range(1, NB_LIEUX)]
        for _ in range(1, self.__taille_pop):
            # Choix de la méthode de création
            r = None
            methode = 'alea' if (random.uniform(0, 1) <= self.__part_alea) else 'glouton'
            # Création d'une route aléatoire
            if methode == 'alea' or len(points_depart_possibles) < 1:
                r = Route(self.__g)
            # Création d'une route gloutonne que l'on va légérement modifier
            else:
                # Si plus aucun point de départ n'est disponible pour la méthode gloutonne 
                # alors on part d'un endroit au hasard et on applique des mutations
                if len(points_depart_possibles) < 1:
                    depart = random.randint(0, NB_LIEUX-1)
                    r = Route(self.__g, methode='glouton', point_depart=depart)
                    nb_swap = random.randint(1, 3)
                    for _ in range(nb_swap): 
                        swap_un   = random.randint(1, NB_LIEUX)
                        swap_deux = random.randint(1, NB_LIEUX)
                        r.swap(swap_un, swap_deux)
                        distance = self.__g.calcul_distance_route(r.getParcours())
                        r.set_distance_totale(distance)
                else:
                    depart = random.choice(points_depart_possibles)
                    points_depart_possibles.remove(depart)
                    r = Route(self.__g, methode='glouton', point_depart=depart)
            # Ajout de la route dans la population
            self.__pop.append(r)
            distance = r.getDistanceTotale()
            # Comparaison avec la meilleure route en mémoire 
            if distance < self.__distance_meilleure_route:
                self.__meilleure_route = r
                self.__distance_meilleure_route = distance

    def evolution(self):
        # TODO
        parent_un   = self.__pop[random.randint(1, NB_LIEUX)]
        parent_deux = self.__pop[random.randint(1, NB_LIEUX)]
        parcours_enfant = croisement(parent_un, parent_deux)
        r = Route(self.__g, parcours=parcours_enfant)
        print(repr(parent_un))
        print(repr(parent_deux))
        print(repr(r))

    def remplacement_population(self, enfants):
        # Fusionne la population parent avec la population enfant
        temp = self.__pop + enfants
        # Tri de la population selon la distance totale
        temp = sorted(temp, key=lambda route: route.get_distance())
        # Prend les 80% meilleurs 


    def main_loop(self):
        # TODO
        pass

    # Opérateurs 
    def __repr__(self):
        output = f'\nTaille Population : {self.__taille_pop}\n'
        output += f'Probabilité de mutation : {self.__proba_mut}\n'
        output += f'Probabilité de croisement : {self.__proba_crois}\n\n'
        for i, route in enumerate(self.__pop):
            output += f'{str(i+1)}) '
            output += repr(route)
            output += '\n\n'
        output += '\nMeilleure route : ' + repr(self.__meilleure_route)

        return output