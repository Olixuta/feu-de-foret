from random import choice,randint

class Meteo:
    def __init__(self) -> None:
        self.orage=False
        self.pluie=False
        self.secheresse=False

    def change_meteo(self,saisons):
        if self.secheresse and saisons.nom=="été":
            return None
        else:
            self.secheresse=False
        proba=randint(1,100)
        if saisons.nom=='hiver' or saisons.nom=='printemps':
            if proba<17:
                self.pluie=True
            else:
                self.pluie=False
        elif saisons.nom=='automne':
            if proba<=50:
                self.pluie=True
            else:
                self.pluie=False
        else:
            if proba<=5:
                self.orage=True
                self.pluie=True
            else:
                self.orage,self.pluie=False,False
            if proba>60:
                self.secheresse=True
    
            
class Vent:
    def __init__(self,orientation,vitesse) -> None:
        self.orientation=orientation
        self.vitesse=vitesse
    def changer_orientation(self):
        orientations=["N","S","E","O","NE","NO","SO","SE"]
        self.orientation=choice(orientations)
    def changer_vitesse(self):
        self.vitesse=randint(0,3)
    def changer_vent(self,saisons):
        self.changer_vitesse()
        if saisons.nom == "hiver":
            self.orientation="N"
        else:
            self.changer_orientation()



dvent1={
    'NO':[(-1,-1)],
    'N':[(-1,0)],
    'NE':[(-1,1)],
    'O':[(0,-1)],
    'E':[(0,1)],
    'SO':[(1,-1)],
    'S':[(1,0)],
    'SE':[(1,1)]   
}

dvent2={
    'NO':[(-1,-1),(-2,-2),(-1,-2),(-2,-1)],
    'N':[(-1,0),(-2,0),(-2,-1),(-2,1)],
    'NE':[(-1,1),(-2,1),(-2,2),(-1,2)],
    'O':[(0,-1),(0,-2),(-1,-2),(1,-2)],
    'E':[(0,1),(0,2),(-1,2),(1,2)],
    'SO':[(1,-1),(2,-2),(1,-2),(2,-1)],
    'S':[(1,0),(2,0),(2,-1),(2,1)],
    'SE':[(1,1),(2,1),(2,2),(1,2)]   
}

dvent3={
    'NO':[(-1,-1),(-2,-2),(-1,-2),(-2,-1),(-3,-2),(-2,-3)],
    'N':[(-1,0),(-2,0),(-2,-1),(-2,1),(-3,0),(-3,-1),(-3,1)],
    'NE':[(-1,1),(-2,1),(-2,2),(-1,2),(-3,2),(2,-3)],
    'O':[(0,-1),(0,-2),(-1,-2),(1,-2),(0,-3),(-1,-3),(1,-3)],
    'E':[(0,1),(0,2),(-1,2),(1,2),(0,3),(-1,3),(1,3)],
    'SO':[(1,-1),(2,-2),(1,-2),(2,-1),(3,-2),(2,-3)],
    'S':[(1,0),(2,0),(2,-1),(2,1),(3,0),(3,-1),(3,1)],
    'SE':[(1,1),(2,1),(2,2),(1,2),(3,2),(2,3)]   
}
liste_vent=[dvent1,dvent2,dvent3]

class Arbre:
    def __init__(self, age ):
        assert type(age)==int and age>=0 
        self.age=age 
        self.feu=False# feu
        self.duree_flamme=0
        self.etat="enfant" # peut prendre en valeur "enfant","adulte", "mort", "terre"
        self.age_sup={"enfant":(5,"adulte"),"adulte":(300,"mort"),"mort":(350,"terre")}
        
    def prend_feu(self):
        self.feu=True
    
    def eteind_feu(self):
        self.feu=False
        self.etat="mort"
        self.duree_flamme=0

    def propagation_depart_feu(self,meteo,cord_arbre,taille,grille):
        if meteo.secheresse and self.etat=="mort": 
            if randint(1,10000)==1:
                self.prend_feu()
                return True
        if self.feu:
            if randint(1,2)==1:
                l=self.positionsArbreVoisins(taille,grille,cord_arbre[0],cord_arbre[1])
                if l!=[]:
                    return choice(l)
        return None # le feu ne se propage pas
    
    def tour_feu(self):
        if self.feu==True:
            self.duree_flamme+=1
            if self.duree_flamme>3:
                self.etat="terre"
                return True
        return False

    def ajout_age(self):
        self.age=self.age+1
        if self.age>self.age_sup[self.etat][0]:
            self.etat=self.age_sup[self.etat][1]
            if self.etat=="terre":
                return True
        return False
        
        

    def cord_valable(self,cord,grille,vent,taille):

        L=[]
        if vent.vitesse==0:
            return [] #il n'aura pas d'enfant car la graine sera sur la même case que l'arbre
        else:
            for tuple in liste_vent[vent.vitesse-1][vent.orientation]:
                if (taille>(cord[0]+tuple[0])>=0 and taille>(cord[1]+tuple[1])>=0) and grille[cord[0]+tuple[0]][cord[1]+tuple[1]]==None:
                    #print(1)
                    L.append(tuple)
        return L
    
    def enfant(self,vent,grille,cord_arbre,taille):
        """plante une graine
        in:
        vent(tuple): 1ere valeur str représentant le sens du vent et 2e valeur un entier entre 0 et 3 représentnt la puissance du vent
        grille(liste de liste): représentant la forêt 
        cord_arbre(tuple): contenant l'indice i et j de l'arbre dans la grille 
        out:
        None si la graine arrive en dehors de la forêt ou sur un arbre
        sinon renvoie les coordonnées de l'enfant de l'arbre 
        """
        assert vent.vitesse>=0 and vent.vitesse<=3
        if self.etat=="adulte":

            l=self.cord_valable(cord_arbre,grille,vent,taille)
            if l!=[]:

                cord=choice(l)
                if grille[cord[0]][cord[1]]==None:

                    return (cord_arbre[0]+cord[0],cord_arbre[1]+cord[1])
        return None
    
    def positionsArbreVoisins(self,taille,grille,i,j):
        l=[]
        pos=[
            (i-1,j-1),(i-1,j),(i-1,j+1),
            (i,j-1),           (i,j+1),
            (i+1,j-1),(i+1,j),(i+1,j+1)
        ]
        for tuple in pos:
            if taille>tuple[0]>=0 and taille>tuple[1]>=0 and grille[tuple[0]][tuple[1]].__class__==Arbre:
                if grille[tuple[0]][tuple[1]].etat != "enfant":
                    l.append(tuple)
        return l
        
    
                    









        

        
        
        