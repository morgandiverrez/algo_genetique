class Lieu:

  # Constructeur 
  def __init__(self, x, y, nom):
    # Coordonnées 
    self.__x   = x
    self.__y   = y
    # Nom 
    self.__nom = nom

  # Getters 
  def getX(self):
    return self.__x
  
  def getY(self):
    return self.__y

  def getNom(self):
    return self.__nom

  # Méthode
  def calcul_distance(self, destination):
    # Récupération des coordonnées de la destination
    x_destination = destination.getX()
    y_destination = destination.getY()

    # Calcul distance au carré x et y
    dist_x = (x_destination - self.__x)**2
    dist_y = (y_destination - self.__y)**2

    return (dist_x + dist_y)**(1/2)
  
  def __repr__(self):
    return f'x={self.__x} \t y={self.__y} \t Nom={self.__nom}'