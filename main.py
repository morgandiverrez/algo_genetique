from classes.affichage  import Affichage
from classes.graph      import Graph
from classes.lieu       import Lieu
from classes.route      import Route
from classes.TSP_GA     import TSP_GA
from classes.constantes import *

if __name__ == '__main__':
    g = Graph('YES')
    tsp_ga = TSP_GA(g, TAILLE_POPULATION, PROBA_MUTATION, PROBA_CROISEMENT, PART_ALEA)
    tsp_ga.main_loop()