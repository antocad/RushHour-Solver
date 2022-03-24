from tkinter import *
from PIL import Image,ImageTk
import time
from RushHour_back import *

TYPES = [Type.ROUGE, Type.H_G_BLEU, Type.H_G_JAUNE, Type.H_G_VERT, Type.H_G_VIOLET, Type.H_P_BLEU, Type.H_P_GRIS, Type.H_P_JAUNE, Type.H_P_MARRON, Type.H_P_ORANGE, Type.H_P_ROSE, Type.H_P_VERT, Type.H_P_VIOLET, Type.V_G_BLEU, Type.V_G_JAUNE, Type.V_G_VERT, Type.V_G_VIOLET, Type.V_P_BLEU, Type.V_P_GRIS, Type.V_P_JAUNE, Type.V_P_MARRON, Type.V_P_ORANGE, Type.V_P_ROSE, Type.V_P_VERT, Type.V_P_VIOLET]

IMAGES = []
PHOTOS = []

def load_photos():
    global IMAGES,PHOTOS
    for i in range(len(TYPES)):
        IMAGES.append(Image.open(TYPES[i].value[1])) #on crée une image python et on la stocke (garde liens dans le tab IMAGES et idem pour PHOTOS)
        if TYPES[i].value[3] == Orientation.HORIZONTAL: #on redimensionne l'image aux tailles des cases
            IMAGES[i] = IMAGES[i].resize((TYPES[i].value[2] * int(SCALE), int(SCALE)), Image.ANTIALIAS)
        else:
            IMAGES[i] = IMAGES[i].resize((int(SCALE), TYPES[i].value[2] * int(SCALE)), Image.ANTIALIAS) 
        PHOTOS.append(ImageTk.PhotoImage(IMAGES[i]))


def view(canvas, voitures):
    canvas.delete("all")
    for i in range(6):
        for j in range(6):
            canvas.create_rectangle(i * SCALE, j * SCALE, i * SCALE + SCALE, j * SCALE + SCALE, fill='gray', outline='white')
    for v in voitures:
        canvas.create_image(v.position[1]*SCALE, v.position[0]*SCALE, anchor=NW, image=PHOTOS[v.id])


def main():
    window = Tk()
    window.title("Rush hour")
    canvas = Canvas(window, width=TAILLE, height=TAILLE)
    canvas.pack()
    
    load_photos()
                
    voitures = [Voiture(Type.ROUGE, [2,1]),
                Voiture(Type.H_P_VERT, [0,0]),
                Voiture(Type.V_G_VIOLET, [1,0]),
                Voiture(Type.V_P_ORANGE, [0,2]),
                Voiture(Type.V_G_JAUNE, [0,3]),
                Voiture(Type.H_G_BLEU, [3,1]),
                Voiture(Type.H_G_VERT, [5,3])]
    
    etatInitial = Etat(voitures)
    solution = parcours_largeur(etatInitial) #solution construite de l'état final à l'état initial
    for e in reversed(solution):
        view(canvas, e.voitures)    #afficher le plateau
        window.update()
        window.update_idletasks()
        time.sleep(0.4)
    print(solution)
    window.update()
    window.update_idletasks()
    window.mainloop()


main()



"""

lvl 1 (982):
[Voiture(Type.ROUGE, [2,1]),
Voiture(Type.H_P_VERT, [0,0]),
Voiture(Type.V_G_VIOLET, [1,0]),
Voiture(Type.V_P_ORANGE, [4,0]),
Voiture(Type.V_G_BLEU, [1,3]),
Voiture(Type.H_G_VERT, [5,2]),
Voiture(Type.V_G_JAUNE, [0,5]),
Voiture(Type.H_P_BLEU, [4,4])]

lvl 11 (791):
[Voiture(Type.ROUGE, [2,1]),
Voiture(Type.V_G_JAUNE, [0,0]),
Voiture(Type.H_P_VERT, [0,1]),
Voiture(Type.V_G_VIOLET, [0,3]),
Voiture(Type.H_G_BLEU, [3,3]),
Voiture(Type.V_P_ORANGE, [3,2]),
Voiture(Type.H_G_VERT, [5,2]),
Voiture(Type.V_P_VIOLET, [4,5])]
    
lvl21 (249):
[Voiture(Type.ROUGE, [2,1]),
Voiture(Type.H_P_VERT, [0,0]),
Voiture(Type.V_G_VIOLET, [1,0]),
Voiture(Type.V_P_ORANGE, [0,2]),
Voiture(Type.V_G_JAUNE, [0,3]),
Voiture(Type.H_G_BLEU, [3,1]),
Voiture(Type.H_G_VERT, [5,3])]

lvl 40 (2810):
[Voiture(Type.ROUGE, [2,3]),
Voiture(Type.H_P_VERT, [0,1]),
Voiture(Type.V_G_VIOLET, [1,5]),
Voiture(Type.V_P_ORANGE, [0,4]),
Voiture(Type.V_G_JAUNE, [0,0]),
Voiture(Type.H_G_BLEU, [3,0]),
Voiture(Type.V_P_BLEU, [1,1]),
Voiture(Type.V_P_ROSE, [1,2]),
Voiture(Type.V_P_VIOLET, [3,3]),
Voiture(Type.V_P_VERT, [4,2]),
Voiture(Type.H_P_MARRON, [5,0]),
Voiture(Type.H_P_JAUNE, [5,3]),
Voiture(Type.H_P_BLEU, [4,4])]
    
HARDEST (13321):
[Voiture(Type.ROUGE, [2,2]),
Voiture(Type.H_G_VIOLET, [0,0]),
Voiture(Type.V_P_BLEU, [0,3]),
Voiture(Type.V_G_BLEU, [0,4]),
Voiture(Type.V_G_JAUNE, [0,5]),
Voiture(Type.V_P_GRIS, [1,0]),
Voiture(Type.H_P_JAUNE, [1,1]),
Voiture(Type.H_P_VERT, [3,0]),
Voiture(Type.V_P_ORANGE, [3,2]),
Voiture(Type.V_P_ROSE, [4,1]),
Voiture(Type.H_P_MARRON, [4,4]),
Voiture(Type.H_P_BLEU, [5,2]),
Voiture(Type.H_P_GRIS, [5,4])]

    """
    
"""lv = [Voiture(Type.ROUGE, [1,1])]
#lv = [Voiture(Type.ROUGE, [2,1]), Voiture(Type.V_G_VIOLET, [2,3])]
e = Etat(lv)
print(e.graph)
for v in lv:
    print(v.liste_deplacements_possibles(e.graph))
print(e.getVoisins())
print("____")
print(parcours_largeur(e))"""

