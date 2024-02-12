from classes.affichage import *
from classes.graph     import *
from classes.lieu      import *
from classes.route     import *

if __name__ == '__main__':
    
    g  = Graph()
    r1 = Route(g)
    r1.generer_route_aleatoire()
    r2 = Route(g)
    r2.generer_route_aleatoire()

    print(repr(g))
    print(repr(r1))
    print(repr(r2))