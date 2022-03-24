import time

class Sommet:
    def __init__(self, abs, ord):
        self.x = abs
        self.y = ord
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def distance(self, C2):

        return (self.x - C2.x)**2 + (self.y - C2.y)**2

    def est_present(self, liste):
        for elem in liste:
            if self.x == elem.x and self.y == elem.y:
                return True
        return False
        
    def equal(self, s2):
        return self.x==s2.x and self.y==s2.y
        
    def voisins(self, map):
        res = []
        if (self.x > 0 and map[self.y][self.x-1]>=0):
            res.append(Sommet(self.x-1, self.y))
        if (self.y > 0 and map[self.y-1][self.x]>=0):
            res.append(Sommet(self.x, self.y-1))
        if ((self.x + 1) < len(map[0]) and map[self.y][self.x+1]>=0):
            res.append(Sommet(self.x+1, self.y))
        if ((self.y + 1) < len(map) and map[self.y+1][self.x]>=0):
            res.append(Sommet(self.x, self.y+1))
        return res

##

class Robot:
    def __init__(self, id, debut, fin, couleur, graphe):
        self.id = id
        self.debut = debut
        self.fin = fin
        self.couleur = couleur
        self.stop = False
        self.graphe = graphe
        self.solutionGen = self.astar() 
        self.solutionGen.reverse() 
        self.pos = debut
        self.indexGen= 0 
        self.solutionCollision = []
        self.indexCol = 0

    def construireSolutionSommets(self, depart, s):
        res = []
        while (s != depart):
            res.append(s)
            s = s.parent
        res.append(depart)
        return res

    def astar(self):
        openlist = [self.debut]
        closedlist = []
        while (openlist != []):
            openlist.sort(key=lambda sommet: sommet.f, reverse=True)
            courante = openlist.pop()
            closedlist.append(courante)
            if courante.equal(self.fin):
                print(self.id, ": solution trouvée")
                return self.construireSolutionSommets(self.debut, courante)
            else:
                listevoisins = courante.voisins(self.graphe)
                for k in listevoisins:
                    if not(k.est_present(closedlist)):
                        if k.est_present(openlist):
                            if not(k.f < openlist[0].f):
                                continue     #on passe au voisin suivant dans le for
                        else:
                            openlist.append(k)
                        k.g = 1 + courante.g
                        k.h = k.distance(self.fin)
                        k.f = k.g + k.h
                        k.parent = courante
        print(self.id, ": Pas de solution")
        self.stop = True
        return []
    
    def avance(self, collision, nbFinished):
        if not self.stop:
            if collision: #s'il y a collision
                
                if len(self.solutionCollision)==self.indexCol:
                    return (False, nbFinished)
                
                #si on est sur le chemin obtenu par le PEL (collision)
                self.pos = self.solutionCollision[self.indexCol]
                self.indexCol += 1
                
            #si le robot tourne sur sa solutionGen de l'A* (pas collision)
            elif (self.indexGen < len(self.solutionGen)):
                self.pos = self.solutionGen[self.indexGen]
                self.indexGen += 1
    
            if self.pos.equal(self.fin):
                self.stop = True
                return (collision, nbFinished+1)
        return (collision, nbFinished)

##

class Mouv:
    def __init__(self, sommet1, sommet2):
        self.s1 = sommet1 #case courante du robot1
        self.s2 = sommet2 #case courante du robot2
        self.parent = None
    
    def equal(self, move2):
        return self.s1.equal(move2.s1) and self.s2.equal(move2.s2)

    def appartient(self, list):
        for m in list:
            if self.equal(m):
                return True
        return False

##

class Organiseur:
    def __init__(self, graphe, duree):
        self.listeRobots = []
        self.collision = False #si vaut True : on déclenche PEL et donc étudie solutionCollision
        self.nbFinished = 0
        self.graphe = graphe
        self.duree = duree

    def start(self, affichage):
        while (self.nbFinished < len(self.listeRobots)):
            self.update()
            affichage.update()
            time.sleep(self.duree)
        print("DONE")

    def update(self):
        if ((not self.collision) and self.check_collision()): #S'IL Y A COLLISION : APPELLE LE PEL
            self.collision = True
            print("collision")
            r1 = self.listeRobots[0]
            r2 = self.listeRobots[1]
            for mouv in self.parcours_largeur(r1, r2): #PEL donne solutionGen comme une liste de Mouv (posr1,posr2)
                r1.solutionCollision.append(mouv.s1) #on donne à r1 sa solutionGen de collision
                r2.solutionCollision.append(mouv.s2) #idem à r2
            r1.indexCol = 0 #On se situe au début de la solutionCollision
            r2.indexCol = 0
        
        for robot in self.listeRobots:
            (self.collision, self.nbFinished) = robot.avance(self.collision, self.nbFinished)


    def check_collision(self):
        """
        renvoie vrai si 2 voitures de la liste l rentrent en collision (si elles sont sur la même case)
        false sinon
        """
        if len(self.listeRobots)<=1 or self.nbFinished>0:
            return False
        r1 = self.listeRobots[0]
        r2 = self.listeRobots[1]
        if(not r1.stop and not r2.stop):
            if ((r1.solutionGen[r1.indexGen].equal(r2.pos) and r1.pos.equal(r2.solutionGen[r2.indexGen])) or (r1.solutionGen[r1.indexGen].equal(r2.solutionGen[r2.indexGen]))):
                return True
        if(r1.stop and not r2.stop and r1.pos.equal(r2.solutionGen[r2.indexGen])):
            return True
        if(r2.stop and not r1.stop and r2.pos.equal(r1.solutionGen[r1.indexGen])):
            return True
        return False
    
    def parcours_largeur(self, robot1, robot2):
        openList = self.mouv_voisins(Mouv(robot1.pos, robot2.pos))
        closedList = []
        while openList != []:
            mouv = openList.pop(0)
            check1 = False
            check2 = False
            posI1 = 0
            posI2 = 0
            for s in robot1.solutionGen[robot1.indexGen:]:
                if mouv.s1.equal(s):
                    check1 = True
                    posI1 = robot1.solutionGen.index(s)+1
                    break
            for s in robot2.solutionGen[robot2.indexGen:]:
                if mouv.s2.equal(s):
                    check2 = True
                    posI2 = robot2.solutionGen.index(s)+1
                    break
                    
            if (check1 and check2):
                robot1.indexGen = posI1
                robot2.indexGen = posI2
                return self.constuireSolutionMouv(Mouv(robot1.pos, robot2.pos), mouv)
            
            closedList.append(mouv)
            for m in self.mouv_voisins(mouv):
                if not(m.appartient(closedList) or m.appartient(openList)):
                    openList.append(m)
        return []
    
    def mouv_voisins(self, etat):
        """
        retourne les positions des robots après le mouvement
        Mouv -> [Mouv] 
        """
        PosRobot1 = etat.s1
        PosRobot2 = etat.s2
        moves = []
        #robot1 bouge + robot2 immobile
        for pos in PosRobot1.voisins(self.graphe):
            if not pos.equal(PosRobot2):
                m = Mouv(pos, PosRobot2)
                m.parent = etat
                moves.append(m)
        #robot2 bouge + robot1 immobile
        for pos in PosRobot2.voisins(self.graphe):
            if not pos.equal(PosRobot1):
                m = Mouv(PosRobot1, pos)
                m.parent = etat
                moves.append(m)
        #robot1 et robot2 bougent
        for pos1 in PosRobot1.voisins(self.graphe):
            for pos2 in PosRobot2.voisins(self.graphe):
                if not pos1.equal(pos2) and not (pos1.equal(PosRobot2) and pos2.equal(PosRobot1)):
                    m = Mouv(pos1, pos2)
                    m.parent = etat
                    moves.append(m)
        return moves
    
    def constuireSolutionMouv(self, depart, Mouv):
        """ Mouv * Mouv -> [Mouv]"""
        res = []
        while (not Mouv.equal(depart)):
            res.append(Mouv)
            Mouv = Mouv.parent
        res.reverse()
        return res
    
    
    def addRobot(self, robot):
        self.listeRobots.append(robot)
    
    def removeRobot(self, robot):
        self.listeRobots.remove(robot)