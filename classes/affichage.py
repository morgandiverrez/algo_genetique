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

    def afficher_lieux(self):
        lieux = self.graph.get_list().copy()
        for lieu in lieux:
            x = lieu.getX()
            y = lieu.getY()
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='blue')
            self.canvas.create_text(x, y, text=lieu.getNom(), fill='white')

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
        output = ''
        for i in range(NB_LIEUX):
            for j in range(NB_LIEUX):
                output += str(self.graph.get_distance(i, j)) + ' '
            output += '\n'
        messagebox.showinfo("Matrice de coûts", output)

    def afficher_meilleures_routes(self, event):
        self.t = self.canvas.create_line(
            *self.get_coords_of_route_from_list_routes(self.tsp_ga.get_n_meilleures_routes(NB_ROUTES_AFFICHER)), fill='grey', dash=(5, 2))

    def quitter_programme(self, event):
        self.master.destroy()
