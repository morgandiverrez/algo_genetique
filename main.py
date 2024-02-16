import tkinter as tk

from classes.affichage import Affichage
from classes.graph     import Graph
from classes.lieu      import Lieu
from classes.route     import Route

if __name__ == '__main__':
    
    g  = Graph()
    r1 = Route(g)
    r1.generer_route_aleatoire()
    r2 = Route(g)
    r2.generer_route_aleatoire()

    root = tk.Tk()
    affichage = Affichage(root, g)
    root.mainloop()