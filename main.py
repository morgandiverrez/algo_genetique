import tkinter as tk

from classes.constantes import *
from classes.affichage import Affichage
from classes.graph     import Graph
from classes.lieu      import Lieu
from classes.route     import Route
from classes.TSP_GA    import TSP_GA

if __name__ == '__main__':
    g = Graph()
    root = tk.Tk()
    tsp_ga = TSP_GA(g, TAILLE_POP, PROBA_MUT, PROBA_CROIS, PART_ALEA)
    affichage = Affichage(root, g, tsp_ga)
    root.mainloop()
    tsp_ga.main_loop()


