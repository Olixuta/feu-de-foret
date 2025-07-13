import pygame
from pygame.locals import*
from math import *
from foretV01 import Arbre,Vent,Meteo
from random import *

pygame.init()

tour_de_vie_monde=0

vent = Vent("E",0)
meteo=Meteo()


# saison : les arbre ne peuvent faire des enfant que le printemp:
class Saison:
    def __init__(self,nom,couleur) -> None:
        self.nom=nom
        self.couleur=couleur
        self.suivante=None

liste_saison=['hiver','printemps','été','automne']
liste_saison_couleur=["#d0e501","#d0e501","#d0e501","#d0e501",
                      "#d0e501","#d0e501","#d0e501","#d0e501",
                      "#d0e501","#d0e501","#d0e501","#d0e501"
                      ,"#d0e501","#d0e501","#d0e501","#d0e501"]
saisons=Saison('hiver',"#ffffff")
saison1=saisons
for i in range(len(liste_saison_couleur)):
    saisons.suivante=Saison(liste_saison[i//4],liste_saison_couleur[i])
    saisons=saisons.suivante
saisons.suivante=saison1.suivante



font = pygame.font.SysFont(None, 24)

screen_width = 1000
screen= pygame.display.set_mode((screen_width+400,screen_width))
pygame.display.set_caption('simulation forêt')

dico_mode = {"arbre":"feu","feu":"pause","pause":"arbre"}
mode = "arbre"
vitesse=100
nb_case=100
taille_case=screen_width/nb_case

# matrice du monde :

monde=[[None for i in range(nb_case)]for j in range(nb_case)]

# affichage

def actualiser_premiere_fois():
    pygame.draw.rect(screen,pygame.Color(saisons.couleur),(0,0,screen_width,screen_width))
    pygame.draw.rect(screen,pygame.Color("white"),(screen_width,0,400,screen_width))
    for i in range(1,nb_case):
        pygame.draw.aaline(screen,"black",(i*taille_case,0),(i*taille_case,screen_width))
        pygame.draw.aaline(screen,"black",(0,i*taille_case),(screen_width,i*taille_case))


actualiser_premiere_fois()
pygame.display.update()

def afficher_arbre(coord,etat):
    vrais_coord=[(coord[0]*taille_case,coord[1]*taille_case)]
    vrais_coord.append((vrais_coord[0][0],vrais_coord[0][1]+taille_case))
    vrais_coord.append((vrais_coord[0][0]+taille_case,vrais_coord[0][1]+taille_case))
    vrais_coord[0]=(vrais_coord[0][0]+taille_case//2,vrais_coord[0][1])
    if etat=="mort":
        pygame.draw.polygon(screen,pygame.Color("#431c02"),vrais_coord)
    elif etat=='feu':
        pygame.draw.polygon(screen,pygame.Color("#fd0000"),vrais_coord)
    else:
        pygame.draw.polygon(screen,pygame.Color("#00bb25"),vrais_coord)

def afficher_graine(coord):
    vrais_coord=(coord[0]*taille_case+taille_case//2,coord[1]*taille_case+taille_case//2)
    pygame.draw.circle(screen,pygame.Color("#e95c00"),vrais_coord,taille_case//4)

# actualisation de l'affichage

def actualiser():
    actualiser_premiere_fois()
    for i in range(nb_case):
        for j in range(nb_case):
            if monde[i][j].__class__==Arbre:
                if monde[i][j].feu==False:
                    if monde[i][j].etat=="adulte":
                        afficher_arbre((i,j),"vivant")
                    elif monde[i][j].etat=="mort":
                        afficher_arbre((i,j),"mort")
                    elif monde[i][j].etat=="terre":
                        monde[i][j]=None   
                    else:
                        afficher_graine((i,j))
                else:
                    afficher_arbre((i,j),"feu")

    # donné affiché
    text = font.render('tour : '+str(tour_de_vie_monde),True,"Black")
    screen.blit(text,(screen_width,0))
    text = font.render('saison : '+saisons.nom,True,"Black")
    screen.blit(text,(screen_width,20))
    text = font.render("vent : orientation : "+ vent.orientation +" vitesse : "+str(vent.vitesse),True,"Black")
    screen.blit(text,(screen_width,40))
    text = font.render("vitesse simulation : "+ str(vitesse),True,"Black")
    screen.blit(text,(screen_width,60))
    text = font.render("mode : "+ mode,True,"Black")
    screen.blit(text,(screen_width,80))
    pygame.display.update()



# boucle de la simulation
temp_clique=pygame.time.get_ticks()
temp_tour=pygame.time.get_ticks()
start=True
while start:
    for event in pygame.event.get():
            # quitter la simulation
            if event.type == pygame.QUIT:
                start=False

            
            if event.type== pygame.KEYDOWN:
                # augmenté la vitesse ou baisser la vitesse de la simulation
                if event.key == K_q:
                    vitesse=vitesse*2
                    actualiser()
                if event.key == K_d:
                    if vitesse>1:
                        vitesse=vitesse//2
                        actualiser()
                # changer de mode :
                if event.key == K_s:
                    mode=dico_mode[mode]
                    actualiser()
                if event.key == K_PAUSE:
                    mode="pause"
                    actualiser()

    # mettre un arbre
    if pygame.mouse.get_pressed(num_buttons=3)[0] and pygame.time.get_ticks()-temp_clique>100:
        temp_clique=pygame.time.get_ticks()
        pos=pygame.mouse.get_pos()
        coord=(round(pos[0]//taille_case),round(pos[1]//taille_case))
        if -1<coord[0]<nb_case and -1<coord[1]<nb_case:
            monde[coord[0]][coord[1]]=Arbre(0)
        actualiser()

    # mettre le feu à un arbre
    if pygame.mouse.get_pressed(num_buttons=3)[2] and pygame.time.get_ticks()-temp_clique>100:
        temp_clique=pygame.time.get_ticks()
        pos=pygame.mouse.get_pos()
        coord=(round(pos[0]//taille_case),round(pos[1]//taille_case))
        if -1<coord[0]<nb_case and -1<coord[1]<nb_case:
            if monde[coord[0]][coord[1]].__class__==Arbre:
                if monde[coord[0]][coord[1]].feu==False:
                    monde[coord[0]][coord[1]].prend_feu()
        print(coord)
        actualiser()


    # mode simulation de croissance de forêt
    if mode == "arbre":
        if pygame.time.get_ticks()-temp_tour>vitesse:
            # changement des variable
            temp_tour=pygame.time.get_ticks()
            tour_de_vie_monde+=1

            # change de saison
            saisons=saisons.suivante
            # change vent
            vent.changer_vent(saisons)
            # change méteo
            meteo.change_meteo(saisons)

            for i in range(nb_case):
                for j in range(nb_case):
                    if monde[i][j].__class__ == Arbre:
                        
                        # feu
                        coord_feu=monde[i][j].propagation_depart_feu(meteo,(i,j),nb_case,monde)
                        if coord_feu:
                            mode="feu"

                        # fait des enfants
                        if saisons.nom == "printemps" and monde[i][j].etat=="adulte":
                            if randint(0,3)==0:
                                coord_graine=monde[i][j].enfant(vent,monde,(i,j),nb_case)
                                if coord_graine != None:
                                    monde[coord_graine[0]][coord_graine[1]]=Arbre(0)
                                    
                        # l'arbre grandi
                        if monde[i][j].ajout_age():
                            monde[i][j]=None
            # change l'affichage
            actualiser()

        # mode simulation d'incendie
    elif mode == "feu":
        if pygame.time.get_ticks()-temp_tour>vitesse:
            temp_tour=pygame.time.get_ticks()
            # change vent
            vent.changer_vent(saisons)
            # compteur des arbre en feu
            compteur=0
            for i in range(nb_case):
                for j in range(nb_case):
                    if monde[i][j].__class__ == Arbre:
                            
                        # feu se propage ou apparait
                        coord_feu=monde[i][j].propagation_depart_feu(meteo,(i,j),nb_case,monde)
                        if coord_feu!=None and coord_feu!=True:
                            monde[coord_feu[0]][coord_feu[1]].prend_feu()

                        if monde[i][j].feu:
                            compteur+=1
                            

                        # le feu brule l'arbre
                        if monde[i][j].tour_feu():
                            monde[i][j]=None
            if compteur==0:
                mode = "arbre"

            # change l'affichage
            actualiser()

