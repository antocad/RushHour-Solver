from tkinter import *
from PIL import Image,ImageTk
from Robots_back import *


class Affichage:
    def __init__(self, graphe, nbLines, nbColumns, scale, organiseur):
        self.graphe = graphe
        self.nbLines = nbLines
        self.nbColumns = nbColumns
        self.scale = scale
        self.organiseur = organiseur
        self.window = Tk()
        self.window.title("Robots : A*  &  PEL")
        self.canvas = Canvas(self.window, width=self.nbColumns*self.scale, height=self.nbLines*self.scale)
        self.canvas.pack()

    def update(self):
        self.viewMAP()
        self.window.update()
        self.window.update_idletasks()

    def drawMap(self):
        for ligne in range(self.nbLines):
            for colonne in range(self.nbColumns):
                if (self.graphe[ligne][colonne] == -1):
                    self.canvas.create_rectangle(colonne * self.scale, ligne * self.scale, colonne * self.scale + self.scale, ligne * self.scale + self.scale, fill='gray', outline='black')                
                elif (self.graphe[ligne][colonne] == 0):
                    self.canvas.create_rectangle(colonne * self.scale, ligne * self.scale, colonne * self.scale + self.scale, ligne * self.scale + self.scale, fill='white', outline='black')
                else:
                    self.canvas.create_rectangle(colonne * self.scale, ligne * self.scale, colonne * self.scale + self.scale, ligne * self.scale + self.scale, fill='yellow', outline='black')
    
    def drawSolution(self, solution, couleur):
        for sommet in solution:
            self.canvas.create_rectangle(sommet.x * self.scale, sommet.y * self.scale, sommet.x * self.scale + self.scale, sommet.y * self.scale + self.scale, fill=couleur, outline='black')
            
    def drawRobot(self, sommet, couleur):
        self.canvas.create_oval( sommet.x * self.scale + self.scale/2 - self.scale/4, 
                            sommet.y * self.scale + self.scale/2 - self.scale/4,
                            sommet.x * self.scale + self.scale/2 + self.scale/4,
                            sommet.y * self.scale + self.scale/2 + self.scale/4,
                            fill=couleur, outline='black')
    
    def drawFin(self, sommet, couleur):
        self.canvas.create_line( sommet.x * self.scale, (sommet.y + 1) * self.scale, (sommet.x + 1) * self.scale, sommet.y * self.scale, fill = couleur, width = 5)
        self.canvas.create_line( sommet.x * self.scale, sommet.y * self.scale, (sommet.x + 1) * self.scale, (sommet.y + 1) * self.scale, fill = couleur, width = 5)
    
    def viewMAP(self):
        self.canvas.delete("all")
        self.drawMap()
        # for robot in self.organiseur.listeRobots:
        #     self.drawSolution(robot.solution, robot.couleur)
        for robot in self.organiseur.listeRobots:    
            self.drawRobot(robot.pos, robot.couleur)
            self.drawFin(robot.fin,robot.couleur)
    


def main():
    '''MAP = [
    [0,  -1],
    [0,  2],
    [0,  -1],
    [0,  -1],
    [0,  -1],
    [0,  -1],
    [0,  1]]
    X_NBCASES = 2 #NB DE COLONNES
    Y_NBCASES = 7 #NB DE LIGNES
    SCALE = 100
    robot1 = Robot(1, Sommet(0,0), Sommet(1,6), 'cyan', MAP)
    robot2 = Robot(2, Sommet(1,6), Sommet(1,1), 'red', MAP)'''
    
    MAP = [
    [1,  -1,  0,  -1,  0],
    [0,  0,  0,   0,  0],
    [-1,  -1,  0,  -1,  0],
    [0,   0,  0,   0,  0],
    [-1, -1,  0,  -1,  0],
    [0,   0,  0,   0,  0],
    [1,  -1,  0,  -1,  0]]
    X_NBCASES = 5 #NB DE COLONNES
    Y_NBCASES = 7 #NB DE LIGNES
    SCALE = 100
    robot1 = Robot(1, Sommet(0,0), Sommet(4,6), 'cyan', MAP)
    robot2 = Robot(2, Sommet(0,6), Sommet(4,0), 'red', MAP)
    
    '''MAP = [
    [1,  -1,  0,  -1,  0],
    [0,  0,  0,   -1,  0],
    [-1,  0,  0,  -1,  0],
    [0,   0,  0,   -1,  0],
    [-1, -1,  -1,  -1,  0],
    [0,   0,  0,   0,  0],
    [0,  -1,  0,  -1,  0]]
    X_NBCASES = 5 #NB DE COLONNES
    Y_NBCASES = 7 #NB DE LIGNES
    SCALE = 100
    robot1 = Robot(1, Sommet(0,0), Sommet(4,6), 'cyan', MAP)'''

    organiseur = Organiseur(MAP, 0.4)
    organiseur.addRobot(robot1)
    organiseur.addRobot(robot2)
    affichage = Affichage(MAP, Y_NBCASES, X_NBCASES, SCALE, organiseur)

    organiseur.start(affichage)
    affichage.window.mainloop()

main()