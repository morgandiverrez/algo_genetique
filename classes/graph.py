import numpy as np 
import csv

from .constantes import *
from .lieu import Lieu
from random import uniform  

class Graph:

  # Constructeur
  def __init__(self, charger_graph=None):
    # Initialisation de la liste vide 
    self.__list_lieux = []
    # Initialisation de la matrice de destination vide 
    self.__matrice_od = np.zeros((NB_LIEUX, NB_LIEUX))
    # Si un graphe a été fourni en entrée alors on le charge
    if charger_graph != None:
      self.charger_graph("data_test/graph_{}.csv".format(NB_LIEUX))
    # Sinon on en créé un aléatoirement
    else:
      # Remplissage aléatoire de la liste des lieux
      for i in range(NB_LIEUX):
        # Création des attributs des différents lieux 
        nom = str(i)
        x   = uniform(0, LARGEUR)
        y   = uniform(0, HAUTEUR)
        # Création des lieux et ajout dans la liste 
        l = Lieu(x, y, nom)
        self.__list_lieux.append(l)
    # Calcul Matrice OD
    self.calcul_matrice_cout_od()

  # Getters 
  def get_list(self):
    return self.__list_lieux

  def get_distance(self, origine, destination):
    return self.__matrice_od[origine][destination]

  # Méthodes 
  def calcul_matrice_cout_od(self):
    # Parcours des lieux
    for origine in range(NB_LIEUX):
      for destination in range(origine):
        # Calcul de la distance entre deux lieux 
        distance = 0
        if origine != destination:
          distance = self.__list_lieux[origine].calcul_distance(self.__list_lieux[destination])
        # Enregistrement de la distance dans la matrice
        self.__matrice_od[origine][destination] = distance
        self.__matrice_od[destination][origine] = distance

  def calcul_distance_route(self, parcours):
        # Initialisation de la distance
        distance_totale = 0
        # Ajout de chaque arc
        for i in range(NB_LIEUX):
            distance_totale += self.get_distance(parcours[i], parcours[i + 1])
        # Retourne la distance totale
        return distance_totale
      
  def plus_proche_voisin(self, indice_lieu, parcours):
    # Initialisation des variables de recherche
    meilleur_voisin   = None
    meilleur_distance = 99999999999

    # Parcours des voisins
    for voisin in range(NB_LIEUX):
      if (voisin != indice_lieu) and (voisin not in parcours):
        distance = self.__list_lieux[indice_lieu].calcul_distance(self.__list_lieux[voisin])
        if distance < meilleur_distance: 
          meilleur_distance = distance
          meilleur_voisin   = voisin

    # Retourne le meilleur voisin
    return meilleur_voisin

  def charger_graph(self, fichier_csv):
    with open(fichier_csv, mode='r') as file:
      csv_reader = csv.reader(file)
      next(csv_reader)
      for  i, row in enumerate(csv_reader):
        x, y = row
        self.__list_lieux.append(Lieu(x = float(x), y = float(y), nom = str(i)))


  def charger_matrice_od(self, fichier_csv):
    self.__matrice_od = pd.read_csv(fichier_csv, header=None).values

  def __repr__(self):
    
    output = 'Liste des lieux : \n'
    for lieu in self.__list_lieux:
      output += lieu.__repr__()
      output += '\n'
    
    output += '\nMatrice Od : \n'
    for ligne in self.__matrice_od:
      for i, distance in enumerate(ligne):
        output += str(round(distance, 2))
        if i < NB_LIEUX - 1:
          output += '\t'
      output += '\n'

    return output