import random 
import tkinter as tk

from .constantes import *
from .route import Route
from .graph import Graph
from .affichage import Affichage

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

        # Nombre d'itération
        self.__nombre_iteration = 0
        self.__nombre_iteration_sans_amelioration = 0
        
    # Getters 
    def get_meilleure_route(self):
        return self.__meilleure_route

    def get_n_meilleures_routes(self, n):
        temp = sorted(self.__pop, key=lambda route: route.getDistanceTotale())
        if temp[0].getDistanceTotale() > self.__distance_meilleure_route:
            temp[n-1] = self.__meilleure_route
            temp = sorted(temp, key=lambda route: route.getDistanceTotale())
        return temp[:n]
    
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
                        swap_un   = random.randint(1, NB_LIEUX-1)
                        swap_deux = random.randint(1, NB_LIEUX-1)
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
        # Création de la population enfant vide 
        taille_pop_enfant = int(self.__proba_crois*self.__taille_pop)
        pop_enfant = []
        # Création des enfants un à un
        amelioration = True
        for _ in range(taille_pop_enfant):
            # Sélection des deux parents 
            parent_un = 0; parent_deux = 0
            while parent_un == parent_deux:
                for i in range(2):
                    # Sélection aléatoire de 3 routes 
                    candidat_un = 0; candidat_deux = 0; candidat_trois = 0
                    while(candidat_un == candidat_deux or candidat_un == candidat_trois or candidat_deux == candidat_trois):
                        candidat_un = random.randint(0, self.__taille_pop-1)
                        candidat_deux = random.randint(0, self.__taille_pop-1)
                        candidat_trois = random.randint(0, self.__taille_pop-1)
                    # Tri en fonction de la distance des candidats
                    classement = sorted([(candidat_un, self.__pop[candidat_un].getDistanceTotale()), 
                                         (candidat_deux, self.__pop[candidat_deux].getDistanceTotale()),
                                         (candidat_trois, self.__pop[candidat_trois].getDistanceTotale())], key=lambda candidat: candidat[1])
                    # Enregistrement dans les parents
                    if i == 0: parent_un   = classement[0][0]
                    else:      parent_deux = classement[0][0] 
            # Croisement des deux parents 
            enfant = croisement(self.__pop[parent_un], self.__pop[parent_deux])
            route_enfant = Route(self.__g, parcours = enfant)
            # Test si l'enfant est meilleur que la meilleure solution 
            if route_enfant.getDistanceTotale() < self.__distance_meilleure_route:
                route_enfant.two_opt(self.__g)
                self.__meilleure_route = route_enfant
                self.__distance_meilleure_route = route_enfant.getDistanceTotale()
                print(f'Amélioration - Iteration {self.__nombre_iteration} : {repr(route_enfant)}')
                amelioration = True
            # Faire les mutations
            if random.uniform(0, 1) <= self.__proba_mut:
                swap_un   = random.randint(1, NB_LIEUX-1)
                swap_deux = random.randint(1, NB_LIEUX-1)
                while(swap_un == swap_deux):
                    swap_un   = random.randint(1, NB_LIEUX-1)
                    swap_deux = random.randint(1, NB_LIEUX-1)
                route_enfant.swap(swap_un, swap_deux)
            # Ajout de l'enfant 
            pop_enfant.append(route_enfant)

        return pop_enfant, amelioration

    def remplacement_population(self, enfants):
        # Fusionne la population parent avec la population enfant
        temp = self.__pop + enfants
        # Tri de la population selon la distance totale
        temp = sorted(temp, key=lambda route: route.getDistanceTotale())
        # Prend les 60% meilleurs 
        nouvelle_population = [temp[idx] for idx in range(0, int(ELITISME*self.__taille_pop))]
        # Comparaison de la meilleure solution actuelle avec celle de l'algorithme
        best_route = nouvelle_population[0]
        amelioration = False
        if nouvelle_population[0].getDistanceTotale() < self.__distance_meilleure_route:
            best_route.two_opt(self.__g)
            self.__meilleure_route = best_route
            self.__distance_meilleure_route = best_route.getDistanceTotale()
            nouvelle_population[0] = best_route
            print(f'Amélioration - Itération { self.__nombre_iteration}: {repr(best_route)}')
            amelioration = True
        # Le reste est séléctionné aléatoirement
        for _ in range(int(ELITISME*self.__taille_pop), self.__taille_pop):
            idx   = random.randint(int(ELITISME*self.__taille_pop), self.__taille_pop-1)
            route = temp[idx] 
            nouvelle_population.append(route)
            temp.remove(route)
        # Remplace l'ancienne population par la nouvelle
        self.__pop = nouvelle_population

        return amelioration

    def main_loop(self):
        # Initialisation de l'affichage 
        root = tk.Tk()
        affichage = Affichage(root, self.__g, self)
        
        # Début de l'algorithme
        self.__nombre_iteration = 0
        self.__nombre_iteration_sans_amelioration = 0
        print(f'Solution de départ : {repr(self.__meilleure_route)}')
        while(self.__nombre_iteration_sans_amelioration < 10000): # TODO mettre une condition d'arrêt (par exemple 10000 itération sans amélioration)
            enfants, amelioration_un = self.evolution()
            amelioration_deux = self.remplacement_population(enfants)
            if amelioration_un or amelioration_deux:
                affichage.update_tsp_ga(self)
                affichage.supprimer_route()
                affichage.afficher_la_meilleure_route()
                self.__nombre_iteration_sans_amelioration = 0
            else:
                self.__nombre_iteration_sans_amelioration += 1
            self.__nombre_iteration += 1
            print(self.__nombre_iteration)
            root.update()
        root.mainloop()

    # Opérateurs 
    def __repr__(self):
        output = f'Solution de départ : {repr(self.__meilleure_route)}'
        output+= f'Amélioration - Itération {self.__nombre_iteration}: {repr(self.__meilleure_route)}'

        return output