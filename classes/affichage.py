import tkinter as tk
import numpy as np

from tkinter import Canvas, Text
from tkinter import messagebox
from random import uniform
from .graph import Graph
from .constantes import *


class Affichage:
    def __init__(self, master, graph, tsp_ga):
        self.master = master
        self.master.title("Affichage - DIVERREZ Morgan / PINON Aurelien / BARRY Caroline")

        self.canvas = Canvas(master, width=LARGEUR, height=HAUTEUR, bg='white')
        self.canvas.pack()

        self.text_area = Text(master, height=5, width=50)
        self.text_area.pack()

        self.graph = graph
        self.tsp_ga = tsp_ga

        # Bind la touche 'ESC' pour quitter le programme
        master.bind('<Escape>', self.quitter_programme)

        # Bind la touche 'M' pour afficher les N meilleures routes trouvées en gris clair
        master.bind('<m>', self.afficher_meilleures_routes)

        # Bind la touche 'C' pour afficher une matrice de coûts de déplacements entre les Lieux
        master.bind('<c>', self.afficher_matrice_couts)

        # Affichage initial des lieux
        self.afficher_lieux()
        self.afficher_text()

    def afficher_lieux(self):
        lieux = self.graph.get_list().copy()
        for lieu in lieux:
            x = lieu.getX()
            y = lieu.getY()
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='blue')
            self.canvas.create_text(x, y, text=lieu.getNom(), fill='white')

    def afficher_text(self):
        self.text_area.delete('1.0', tk.END)

        # Récupérer l'évolution des étapes des algorithmes
        evolution_algo = repr(self.tsp_ga)  # Remplacez ceci par votre méthode d'obtention de l'évolution

        # Afficher l'évolution dans la zone de texte
        self.text_area.insert(tk.END, evolution_algo)

    def get_coords_of_route_from_list_routes(self, list_routes):
        routes_coords = []
        for route in list_routes[1:]:
            coords_of_route = self.get_coords_from_route(route)
            routes_coords.extend(coords_of_route)
        return routes_coords

    def get_coords_from_route(self, route):
        coords = []
        lieux = self.graph.get_list().copy()
        for indice in route.getParcours():
            x = lieux[indice].getX()
            y = lieux[indice].getY()
            coords.extend((x, y))
        return coords

    def afficher_matrice_couts(self, event):
        # Créer une nouvelle fenêtre pour afficher la matrice de coût
        fenetre_matrice = tk.Toplevel(self.master)
        fenetre_matrice.title("Matrice de Coût")

        # Récupérer la matrice de coût
        matrice_cout = self.graph.get_matrice_od()  # Remplacez ceci par votre méthode d'obtention de la matrice de coût

        # Afficher la matrice de coût dans un tableau dans la nouvelle fenêtre
        for i in range(len(matrice_cout)):
            for j in range(len(matrice_cout[i])):
                label = tk.Label(fenetre_matrice, text=round(matrice_cout[i][j], 1), borderwidth=1, relief="solid",
                                 width=10,
                                 height=2)
                label.grid(row=i, column=j)

    def afficher_meilleures_routes(self, event):
        self.t = self.canvas.create_line(
            *self.get_coords_of_route_from_list_routes(self.tsp_ga.get_n_meilleures_routes(NB_ROUTES_AFFICHER)), fill='grey', dash=(5, 2))
        
    def afficher_la_meilleure_route(self):
        self.t = self.canvas.create_line(
            *self.get_coords_from_route(self.tsp_ga.get_meilleure_route()), fill='blue', tags='route')
        #afficher ordre passage meilleur route
        lieux = self.graph.get_list().copy()
        for i, indice in enumerate(self.tsp_ga.get_meilleure_route().getParcours()):
            x = lieux[indice].getX()
            y = lieux[indice].getY()
            self.canvas.create_text(x+20, y, text=i, fill='blue')

    def supprimer_route(self):
        self.canvas.delete("route")
        
    def update_tsp_ga(self, tsp_ga):
        self.tsp_ga = tsp_ga

    def quitter_programme(self, event):
        self.master.destroy()