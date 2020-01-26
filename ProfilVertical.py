#!usr/bin/env python
#-*- coding:utf-8 -*-
#
class ProfilVertical:
    def __init__ (self,x):  # x est une liste de tuples (nivAuDessusDuSol,valeur) pas forcément classée
        self.x=x
    def affiche(self):
        print (self.x)
    def getKey(self,item):
        return item[0]
    def rechercheNiveauDuValref(self,valref):
        # tri des tuples (niv,val) par niveaux croissants
        xtrie=sorted(self.x, key=self.getKey)
        print (xtrie)
        print (valref)
        # recherche, en partant du niveau le plus bas, du premier franchissement de "valref" en décroissant
        valprec=xtrie[0][1]
        nivprec=xtrie[0][0]
        for x in xtrie:
            #print x
            if ((x[1]<valref) and (x[1]<valprec)) : break
            valprec=x[1]
            nivprec=x[0]
        print (nivprec,valprec,x[0],x[1])
        niv=nivprec+(x[0]-nivprec)*(valprec-valref)/(valprec-x[1])
        print (niv)
        return (niv)
            
x=ProfilVertical([(100,2),(200,4),(50,56),(425,-12),(660,1253),(35,100),(60,-3),(53,-12)])
x.affiche()
x.rechercheNiveauDuValref(600.0)