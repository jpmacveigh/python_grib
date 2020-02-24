 # Voir : https://mf-models-on-aws.org/
#INPUT=  "AROME_010_SP1_06H_201702040000.grib2"
#INPUT=  "AROME_0.025_SP1_00H06H_201510131800.grib2"
#INPUT=  "AROME_0.025_SP2_19H24H_201510131800.grib2"
#INPUT = "arpege-world_20200113_00_UGRD_agl_42h.grib2"
#INPUT=  "cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2"
import datetime
import sys
sys.path.insert(0,'/home/ubuntu/environment/node_jpmv/WCS_MF') # insérer dans sys.path le dossier contenant le ou les modules
from util_eccodes import *

'''
u=get_une_valeur_brute ("arpege-world","UGRD","10m",echeance=6,rang_message=0,rang_valeur=250)
v=get_une_valeur_brute ("arpege-world","VGRD","10m",echeance=6,rang_message=0,rang_valeur=250)
ventUV=VentHorizontal(u,v)
ff=get_une_valeur_brute ("arpege-world","WIND","10m",echeance=6,rang_message=0,rang_valeur=250)
dd=get_une_valeur_brute ("arpege-world","WDIR","10m",echeance=6,rang_message=0,rang_valeur=250)
ventDDFF=VentHorizontal_DDFF(dd,ff)
print(ff,ventUV.vitesse_ms())
print(dd,ventUV.direction())
print (u,ventDDFF.u)
print (v,ventDDFF.v)

assert abs(ventUV.vitesse_ms()-ff)<=10**-1 , (ventUV.vitesse_ms(),ff)
assert abs(ventUV.direction()-dd)<=10**-1  ,(ventUV.direction(),dd)
'''
code_model="arpege-world"
#code_model="arome-france"
#code_model="arome-france-hd"

'''

print(get_les_niveaux_now_disponibles(code_model,"TMP"))
print(get_les_niveaux_now_disponibles(code_model,"WIND"))
print(get_les_niveaux_now_disponibles(code_model,"WDIR"))
print(get_les_niveaux_now_disponibles(code_model,"UGRD"))
print(get_les_niveaux_now_disponibles(code_model,"VGRD"))
print(get_les_niveaux_now_disponibles(code_model,"PRES"))
print(get_les_niveaux_now_disponibles(code_model,"CAPE"))
print(get_les_niveaux_now_disponibles(code_model,"GP"))
print(get_les_niveaux_now_disponibles(code_model,"HPBL"))

'''
Lille=(3.06,50.3)
Everest=(86.925,27.989)
Atlantique_Nord=(-43.713,31.535)
Ajaccio=(8.792,41.919)
lieu=Lille
#lieu=Ajaccio
'''
profil_vertical=get_now_profil_vertical_complet(code_model,"WDIR",lieu[0],lieu[1])
for i in range(len(profil_vertical)):
    print (i,profil_vertical[i][1],profil_vertical[i][2])

profil_vertical=get_now_profil_vertical_complet(code_model,"WIND",lieu[0],lieu[1])
for i in range(len(profil_vertical)):
    print (i,profil_vertical[i][1],profil_vertical[i][2])   
exit()

profil_vertical_vent_horizontal=get_now_profil_vent_horizontal(code_model,lieu[0],lieu[1])
for i in range(len(profil_vertical_vent_horizontal)):
    print (i,profil_vertical_vent_horizontal[i][0],profil_vertical_vent_horizontal[i][1],profil_vertical_vent_horizontal[i][2]) 

exit()
'''
import random
print(datetime.datetime.now())

for i in range(10):
    altitude=float(random.randint(10,12000))
    print (i,datetime.datetime.now(),altitude,get_now_vent_arpege_world (lieu[0],lieu[1],altitude))

exit()

'''
vent=get_now_vent_horizontal(code_model,lieu[0],lieu[1],12000.)
vent[2].affiche_tout()



#print (valeur_now_num_niveau("arpege-world","TMP","2m",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","PRES","msl",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","GP","agl",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","GP","isobaric",lieu[0],lieu[1],0))

exit()
#print (valeur_now_num_niveau("arpege-world","UGRD","10m",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","VGRD","10m",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","WDIR","10m",lieu[0],lieu[1],0))
#print (valeur_now_num_niveau("arpege-world","WIND","10m",lieu[0],lieu[1],0))
vent= get_vent_horizontal_now("arpege-world","10m",lieu[0],lieu[1],0)
print (vent)
print (vent["valeur"].toStringKmh(),vent["valeur"].u,vent["valeur"].v)
exit()

print (" ** Nombre de messages grib dans le fichier grib2 : ",len(messages))
n=1
for msg in messages : 
    print (n,msg["nameECMF"],msg["level"],msg["typeOfLevel"],msg.date_run,msg.echeance,msg.date_previ,value(msg,lieu[0],lieu[1]))
    n=n+1
exit()

for k in messages[0].keys():
    print (k," : ",msg[k])
'''      