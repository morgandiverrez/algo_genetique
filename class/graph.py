LARGEUR = 800
HAUTEUR = 600
NB_LIEUX = 5


class Graph:

    # Constructeur
    def __init__(self):
        # Initialisation de la liste vide
        self.__list_lieux = []
        # Initialisation de la matrice de destination vide
        self.__matrice_od = np.zeros((NB_LIEUX, NB_LIEUX))
        # Remplissage aléatoire de la liste des lieux
        for i in range(NB_LIEUX):
            # Création des attributs des différents lieux
            nom = 'lieu_' + str(i + 1)
            x = uniform(0, LARGEUR)
            y = uniform(0, HAUTEUR)
            # Création des lieux et ajout dans la liste
            l = Lieu(x, y, nom)
            self.__list_lieux.append(l)

    # Méthodes
    def calcul_matrice_cout_od(self):
        # Parcours des lieux
        for origine in range(NB_LIEUX):
            for destination in range(NB_LIEUX):
                # Calcul de la distance entre deux lieux
                distance = 0
                if origine != destination:
                    distance = self.__list_lieux[origine].calcul_distance(destination)
                # Enregistrement de la distance dans la matrice
                self.__matrice_od[origine][destination] = distance

    def plus_proche_voisin(self, indice_lieu):
        # Initialisation des variables de recherche
        meilleur_voisin = None
        meilleur_distance = 99999999999

        # Parcours des voisins
        for voisin in range(NB_LIEUX):
            if voisin != indice_lieu:
                distance = self.__list_lieux[indice_lieu].calcul_distance(voisin)
                if distance < meilleur_distance:
                    meilleur_distance = distance
                    meilleur_voisin = voisin

        # Retourne le meilleur voisin
        return meilleur_voisin

    def charger_graph(self):
        # TODO
        pass

    def charger_matrice_od(self):
        # TODO
        pass