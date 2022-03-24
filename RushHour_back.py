from enum import Enum
import copy

NBCASES = 6
TAILLE = 640
SCALE = TAILLE/NBCASES


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Type(Enum):
    ROUGE       = (0, "./IMG/rouge.png",       2, Orientation.HORIZONTAL)
    H_G_BLEU    = (1, "./IMG/HG_bleu.png",     3, Orientation.HORIZONTAL)
    H_G_JAUNE   = (2, "./IMG/HG_jaune.png",    3, Orientation.HORIZONTAL)
    H_G_VERT    = (3, "./IMG/HG_vert.png",     3, Orientation.HORIZONTAL)
    H_G_VIOLET  = (4, "./IMG/HG_violet.png",   3, Orientation.HORIZONTAL)
    H_P_BLEU    = (5, "./IMG/HP_bleu.png",     2, Orientation.HORIZONTAL)
    H_P_GRIS    = (6, "./IMG/HP_gris.png",     2, Orientation.HORIZONTAL)
    H_P_JAUNE   = (7, "./IMG/HP_jaune.png",    2, Orientation.HORIZONTAL)
    H_P_MARRON  = (8, "./IMG/HP_marron.png",   2, Orientation.HORIZONTAL)
    H_P_ORANGE  = (9, "./IMG/HP_orange.png",   2, Orientation.HORIZONTAL)
    H_P_ROSE    = (10, "./IMG/HP_rose.png",     2, Orientation.HORIZONTAL)
    H_P_VERT    = (11, "./IMG/HP_vert.png",     2, Orientation.HORIZONTAL)
    H_P_VIOLET  = (12, "./IMG/HP_violet.png",   2, Orientation.HORIZONTAL)
    V_G_BLEU    = (13, "./IMG/VG_bleu.png",     3, Orientation.VERTICAL)
    V_G_JAUNE   = (14, "./IMG/VG_jaune.png",    3, Orientation.VERTICAL)
    V_G_VERT    = (15, "./IMG/VG_vert.png",     3, Orientation.VERTICAL)
    V_G_VIOLET  = (16, "./IMG/VG_violet.png",   3, Orientation.VERTICAL)
    V_P_BLEU    = (17, "./IMG/VP_bleu.png",     2, Orientation.VERTICAL)
    V_P_GRIS    = (18, "./IMG/VP_gris.png",     2, Orientation.VERTICAL)
    V_P_JAUNE   = (19, "./IMG/VP_jaune.png",    2, Orientation.VERTICAL)
    V_P_MARRON  = (20, "./IMG/VP_marron.png",   2, Orientation.VERTICAL)
    V_P_ORANGE  = (21, "./IMG/VP_orange.png",   2, Orientation.VERTICAL)
    V_P_ROSE    = (22, "./IMG/VP_rose.png",     2, Orientation.VERTICAL)
    V_P_VERT    = (23, "./IMG/VP_vert.png",     2, Orientation.VERTICAL)
    V_P_VIOLET  = (24, "./IMG/VP_violet.png",   2, Orientation.VERTICAL)

#_______________________________________________________________________________

class Voiture:
    def __init__(self, type, position):
        self.type = type
        self.taille = type.value[2]
        self.orientation = type.value[3]
        self.position = position
        self.id = type.value[0]


    def deplacement(self, n):
        if self.orientation == Orientation.HORIZONTAL:
            self.position[1] += n
        else :
            self.position[0] += n

    def liste_deplacements_possibles(self, graph):
        deplacementsPossibles = []
        x,y = self.position
        cpt = 0
        if self.orientation == Orientation.HORIZONTAL:
            while y > 0 and graph[x][y-1] == -1:
                cpt = cpt-1
                deplacementsPossibles.append(cpt)
                y = y-1
            x,y = self.position
            cpt = 0
            while y + self.taille < NBCASES and graph[x][y+self.taille] == -1:
                cpt = cpt+1
                deplacementsPossibles.append(cpt)
                y=y+1
        else:
            while x > 0 and graph[x-1][y] == -1:
                cpt = cpt-1
                deplacementsPossibles.append(cpt)
                x = x-1
            x,y = self.position
            cpt = 0
            while x + self.taille < NBCASES and graph[x+self.taille][y] == -1:
                cpt = cpt+1
                deplacementsPossibles.append(cpt)
                x = x+1
        return deplacementsPossibles

#______________________________________________________________________________________


def list2graph(voitures):
    graph = [[-1 for j in range(NBCASES)] for i in range(NBCASES)]
    for v in voitures:
        x,y = v.position
        if v.orientation == Orientation.HORIZONTAL:
            for k in range(y,y+v.taille):
                graph[x][k] = v.id
        else:
            for k in range(x,x+v.taille):
                graph[k][y] = v.id
    return graph



class Etat:
    def __init__(self, listeVoitures):
        self.voitures = listeVoitures
        self.parent = None
        self.graph = list2graph(listeVoitures)

    def estFinal(self):
        return (self.graph[2][5] == 0)

    def deplacerVoiture(self, indiceVoiture, n):
        self.voitures[indiceVoiture].deplacement(n)
        self.graph = list2graph(self.voitures)

    def recupereVoisins(self):
        ListeVoisins = []
        for v in self.voitures:
            deplacementsPossibles = v.liste_deplacements_possibles(self.graph)
            for d in deplacementsPossibles:
                etatcopie = copy.deepcopy(self)
                etatcopie.deplacerVoiture(self.voitures.index(v), d)
                etatcopie.parent = self
                ListeVoisins.append(etatcopie)
        return ListeVoisins

def retrouverSolution(etatfinal,etatinitial):
    solution = []
    etatcourant = etatfinal
    while etatcourant != etatinitial:
        solution.append(etatcourant)
        etatcourant = etatcourant.parent
    solution.append(etatinitial)
    return solution

def egale(mat, g):
    n = len(mat)

    for i in range(n):
        for j in range(n):
            if g[i][j] != mat[i][j]:
                return False
    return True

def appartient(mat,liste):
    for g in liste:
        if egale(g, mat):
            return True
    return False


def parcours_largeur(etatInitial):
    noeudsAExplorer = [etatInitial] #openlist
    noeudsDejaExplores = []         #closedlist

    if etatInitial.estFinal():
        print("solution trouvée: 0  mouvement")
        return [etatInitial]

    while noeudsAExplorer != []:
        etatcourant = noeudsAExplorer.pop(0)
        if not (appartient(etatcourant.graph,noeudsDejaExplores)):
            noeudsDejaExplores.append(etatcourant.graph)
        voisins = etatcourant.recupereVoisins()
        print(len(noeudsDejaExplores))
        for v in voisins:
            if not (appartient(v.graph,noeudsDejaExplores) or appartient(v.graph, [n.graph for n in noeudsAExplorer])):
                if v.estFinal():
                    res = retrouverSolution(v,etatInitial)
                    print("solution trouvée:",len(res)-1,"mouvements")
                    return res
                noeudsAExplorer.append(v)
    print("solution non trouvée")
    return []
    
    