class Route:
    def __init__(self, graph):
        self.graph = graph
        self.ordre = []

    def generer_route_aleatoire(self):
        self.ordre = [0]  # Début toujours au lieu 0
        lieux_disponibles = self.graph.liste_lieux.copy()
        lieux_disponibles.pop(0)  # Retirer le premier lieu, déjà visité
        random.shuffle(lieux_disponibles)
        self.ordre.extend([int(lieu.nom) for lieu in lieux_disponibles])
        self.ordre.append(0)  # Retour au lieu de départ

    def calcul_distance_route(self):
        distance_totale = 0
        for i in range(len(self.ordre) - 1):
            distance_totale += self.graph.matrice_od[self.ordre[i]][self.ordre[i + 1]]
        return distance_totale