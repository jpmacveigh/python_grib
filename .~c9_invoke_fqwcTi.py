# Voir : https://mf-models-on-aws.org/
#INPUT=  "AROME_010_SP1_06H_201702040000.grib2"
#INPUT=  "AROME_0.025_SP1_00H06H_201510131800.grib2"
#INPUT=  "AROME_0.025_SP2_19H24H_201510131800.grib2"
#INPUT = "arpege-world_20200113_00_UGRD_agl_42h.grib2"
#INPUT=  "cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2"
from eccodes import *
import numpy as np
from scipy import interpolate
import datetime
import requests
import sys
sys.path.insert(0,'/home/ubuntu/environment/node_jpmv/WCS_MF') # insérer dans sys.path le dossier contenant le/les modules
from VentHorizontal import VentHorizontal
from VentHorizontal_DDFF import VentHorizontal_DDFF
les_modeles_MF={      # le pas de temps des sorties de chaque modèle (1 ou 3 heures)
    "arome-france-hd":{"dt-sorties-heures":1},
    "arome-france":{"dt-sorties-heures":1},
    "arpege-europe":{"dt-sorties-heures":1},
    "arpege-world":{"dt-sorties-heures":3}}
def assert_code_model(code_model):
    assert code_model in les_modeles_MF.keys() , code_model

def les_dates_de_sortie_entourant_now_dans_le_temps (code_model):
    assert_code_model(code_model)
    date_to_load=get_date_to_load()
    now_UTCtimestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())
    now_UTCdate = datetime.datetime.utcfromtimestamp(now_UTCtimestamp)
    i=0
    date=get_date_to_load()
    while (i in range(23)) and (date<now_UTCdate) :
        date=date+datetime.timedelta(hours=les_modeles_MF[code_model]["dt-sorties-heures"])
        i=i+1
    date_before=date-datetime.timedelta(hours=les_modeles_MF[code_model]["dt-sorties-heures"])
    echeance_before=(i-1)*les_modeles_MF[code_model]["dt-sorties-heures"]
    date_after=date
    date_before_timestamp=datetime.datetime.timestamp(date_before)
    date_after_timestamp=datetime.datetime.timestamp(date_after)
    echeance_after=echeance_before+les_modeles_MF[code_model]["dt-sorties-heures"]
    prop=(now_UTCtimestamp-date_before_timestamp)/(date_after_timestamp-date_before_timestamp)
    return(date_to_load,date_before,echeance_before,date_after,echeance_after,prop)

def get_entourants_grib_messages (code_model,code_param,code_type_niv):    
    assert_code_model(code_model)
    (date_to_load,_,echeance_before,_,echeance_after,prop)=les_dates_de_sortie_entourant_now_dans_le_temps(code_model)
    url_before = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_before)
    url_after  = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_after)
    return (date_to_load,get_grib_messages_from_url(url_before),get_grib_messages_from_url(url_after),prop)

def get_grib_messages (code_model,code_param,code_type_niv,echeance):
    url=get_grib_url_to_load(code_model,code_param,code_type_niv,echeance)
    print (url)
    return(get_grib_messages_from_url(url))

def get_une_valeur_brute (code_model,code_param,code_type_niv,echeance,rang_message,rang_valeur):
    grib_messages=get_grib_messages (code_model,code_param,code_type_niv,echeance)
    return (grib_messages[rang_message]["values"][rang_valeur])

def get_grib_url_to_load(code_model,code_param,code_type_niv,echeance):
        # Exemple d'url :  https://mf-nwp-models.s3.amazonaws.com/arpege-world/v2/2020-01-17/00/RH/agl/0h.grib2
        date_to_load=get_date_to_load()
        code_jour=str(date_to_load.date())
        code_heure="%02d" % date_to_load.hour
        url="https://mf-nwp-models.s3.amazonaws.com/"+code_model+"/v2/"
        url=url+code_jour+"/"+code_heure+"/"     
        url=url+code_param+"/"+code_type_niv+"/"  # 
        url=url+str(echeance)+"h"
        url=url+".grib2"
        return (url)
    
def get_date_to_load():    #  determine l'heure du RUN le plus récent à télécharger. Pour les 4 modèles : 00,06,12 ou 18 UTC
    now_UTCtimestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())
    now_UTCdate = datetime.datetime.utcfromtimestamp(now_UTCtimestamp)
    now_UTChour = now_UTCdate.time().hour
    zero_heure=datetime.time(0)
    today=datetime.datetime.combine(now_UTCdate,zero_heure)
    jour=today
    if (now_UTChour <= 4):
        heure=18
        hier=today-datetime.timedelta(days=1)
        jour=hier
    elif (4 < now_UTChour <= 10):
        heure=0
    elif (10 < now_UTChour <= 16):
        heure=6
    elif (16 < now_UTChour <= 22):
        heure=12
    else:
        heure=18
    return (jour+datetime.timedelta(hours=heure))
    
def get_grib_messages_from_url(url):
    #print (url)
    r=requests.get(url)
    assert (r.status_code == 200), str(r.status_code)+"  "+ url
    fichier = open("tempo.grib2", "wb")
    fichier.write(r.content)
    fichier.close()
    grib=GribFile("tempo.grib2")
    check=False
    messages=[]
    def construct_times():  # ajoute un paramètre "date_previ" 
        date_run= datetime.datetime(msg["year"],msg["month"],msg["day"],msg["hour"],msg["minute"],msg["second"])
        msg.date_run=date_run
        echeance=msg["forecastTime"]
        msg.echeance=echeance
        an=   int(str(msg["validityDate"])[0:4])
        mois= int(str(msg["validityDate"])[4:6])
        jour= int(str(msg["validityDate"])[6:8])
        heure=int(msg["validityTime"]/100)
        date_previ=datetime.datetime(an,mois,jour,heure)
        msg.date_previ=date_previ
        assert date_run+datetime.timedelta(hours=echeance)==date_previ,(date_run,date_previ,echeance)
    for i in range(len(grib)):
        msg=GribMessage(grib)
        if check :
            assert msg["identifier"]=="GRIB"
            assert msg["GRIBEditionNumber"]== 2
            nbTotalValues=len(msg["values"])
            nx=msg["Ni"]
            ny=msg["Nj"]
            assert (nx*ny)==nbTotalValues
            assert len(msg["distinctLongitudes"])==nx
            assert len(msg["distinctLatitudes"])==ny
            assert msg["getNumberOfValues"]==nbTotalValues
            assert len(msg["latitudes"])==nbTotalValues
            assert len(msg["longitudes"])==nbTotalValues  
        construct_times()  # Controle et ajout des dates, heures et echeance du message GRIB 
        messages.append(msg)
    return (messages)
    
def valeur_now_num_niveau (code_model,code_param,code_type_niv,longitude,latitude,num_niveau):
    (date_to_load,grib_messages_avant,grib_messages_apres,prop)=get_entourants_grib_messages(code_model,code_param,code_type_niv)
    # on traite pour le moment premier niveau et on n'utilise pas l'argument "niveau" TODO
    message_avant=grib_messages_avant[num_niveau]
    message_apres=grib_messages_apres[num_niveau]
    val_avant=value(message_avant,longitude,latitude)
    val_apres=value(message_apres,longitude,latitude)
    valeur_now= (val_avant*prop+(1-prop)*val_apres)
    #print (val_avant,val_apres,prop,valeur_now)
    rep={}
    rep["run"]=date_to_load
    rep["param"]=code_param
    rep["type_niv"]=message_avant["typeOfLevel"]
    rep["longi"]=longitude
    rep["lati"]=latitude
    rep["niv"]=message_avant["level"]
    rep["valeur"]=valeur_now
    return (rep)
    
  
def value(msg_grib,longitude,latitude):   # interpolation en un point quelconque de la grille d'un messsage Grib
    assert -180.<=longitude<=180. , longitude
    assert -90.<=latitude<=90. , latitude
    def longitude_360(longitude):  # transforme une longitude dans [-180,180] en une dans [0,360]
        #assert -180.<=longitude<=180. , longitude
        return ((longitude+360.)%360.)
    if not ("interpolateur" in msg_grib) :
        les_longitudes=np.array(msg_grib["distinctLongitudes"])
        les_latitudes=np.array(msg_grib["distinctLatitudes"])
        valeurs_sur_la_grille=np.reshape(msg_grib["values"],(msg_grib["Ni"],msg_grib["Nj"]),order="F")
        func=interpolate.interp2d(les_latitudes,les_longitudes,valeurs_sur_la_grille)
        msg_grib.interpolateur=func
    return (msg_grib.interpolateur(latitude,longitude_360(longitude))[0])

def get_altitude_terrain(code_model,longitude,latitude):
    assert_code_model(code_model)
    def get_terrain(code_model):
        #url="https://mf-models-on-aws.org/#"+code_model+"/static/terrain.grib2"
        url="https://mf-nwp-models.s3.amazonaws.com/"+code_model+"/static/terrain.grib2"
        return get_grib_messages_from_url(url)
    msg=get_terrain(code_model)
    return value(msg[0],longitude,latitude)

def get_nature_terrain(code_model,longitude,latitude):
    assert_code_model(code_model)
    def get_landmask(code_model):
        url="https://mf-nwp-models.s3.amazonaws.com/"+code_model+"/static/landmask.grib2"
        return get_grib_messages_from_url(url)
    msg=get_landmask(code_model)
    return value(msg[0],longitude,latitude)
    
def get_vent_horizontal_now (code_model,code_type_niv,longitude,latitude,num_niveau):
    dd=valeur_now_num_niveau(code_model,"WDIR",code_type_niv,longitude,latitude,num_niveau)
    ff=valeur_now_num_niveau(code_model,"WIND",code_type_niv,longitude,latitude,num_niveau)
    rep={}
    rep["run"]=dd["run"]
    rep["param"]="VENT HORIZONTAL"
    rep["type_niv"]=dd["type_niv"]
    rep["longi"]=longitude
    rep["lati"]=latitude
    rep["niv"]=dd["niv"]
    rep["valeur"]=VentHorizontal_DDFF(dd["valeur"],ff["valeur"])
    return (rep)
def get_les_niveaux_now_disponibles(code_model,code_param):
    les_niveaux_possibles=["agl","isobaric","10m","2m","atmosphere","surface","msl"]  # voir : https://mf-models-on-aws.org/
    (date_to_load,date_before,echeance_before,date_after,echeance_after,prop)=les_dates_de_sortie_entourant_now_dans_le_temps(code_model)
    rep={}
    rep["code_model"]=code_model
    rep["code_param"]=code_param
    les_niveaux_disponibles=[]
    for code_type_niveau in les_niveaux_possibles:
        #https://mf-nwp-models.s3.amazonaws.com/arpege-world/v2/2020-01-26/06/TMP/agl/42h.grib2.inv
        #https://mf-nwp-models.s3.amazonaws.com/arpege-world/v2/2020-01-26/06/TMP/agl/6h.grib2.inv
        #https://mf-nwp-models.s3.amazonaws.com/arpege-world/v2/2020-01-26/06/TMP/agl/6h.grib2.inv
        url=get_grib_url_to_load(code_model,code_param,code_type_niveau,echeance_before)
        url=url+".inv"
        r=requests.get(url)
        if (r.status_code==200): 
            les_niveaux_disponibles.append(code_type_niveau)
            list=r.text.split('\n')
            les_niveaux=[]
            for ligne in list:
                slist=ligne.split(':')
                les_niveaux.append(slist[4])
            rep[code_type_niveau]=les_niveaux
    rep["les_niveaux_now_disponibles"]=les_niveaux_disponibles
    return(rep)

def get_now_profil_vertical (code_model,code_param,longitude,latitude):
    les_niveaux_now_disponibles=get_les_niveaux_now_disponibles(code_model,code_param)
    for code_type_niv in les_niveaux_now_disponibles["les_niveaux_now_disponibles"]:
        print (code_type_niv,len(les_niveaux_now_disponibles[code_type_niv]))
        (date_to_load,grib_messages_before,grib_messages_after,prop)=get_entourants_grib_messages (code_model,code_param,code_type_niv)
        for i in range(len(les_niveaux_now_disponibles[code_type_niv])):
            print(i)
            msg_grib_before=grib_messages_before[i]
            val_before=value(msg_grib_before,longitude,latitude)
            print (val_before,les_niveaux_now_disponibles[code_type_niv][i])
            msg_grib_after=grib_messages_after[i]
            val_after=value(msg_grib_after,longitude,latitude)
            print (val_after,les_niveaux_now_disponibles[code_type_niv][i])
    return (0)
         
    


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



print(get_les_niveaux_now_disponibles(code_model,"TMP"))
print(get_les_niveaux_now_disponibles(code_model,"WIND"))
print(get_les_niveaux_now_disponibles(code_model,"WDIR"))
print(get_les_niveaux_now_disponibles(code_model,"UGRD"))
print(get_les_niveaux_now_disponibles(code_model,"VGRD"))
print(get_les_niveaux_now_disponibles(code_model,"PRES"))
print(get_les_niveaux_now_disponibles(code_model,"CAPE"))
print(get_les_niveaux_now_disponibles(code_model,"GP"))
print(get_les_niveaux_now_disponibles(code_model,"HPBL"))




Lille=(3.06,50.3)
Everest=(86.925,27.989)
Atlantique_Nord=(-43.713,31.535)
lieu=Lille

get_now_profil_vertical(code_model,"WDIR",lieu[0],lieu[1])

exit()


print (valeur_now_num_niveau("arpege-world","TMP","2m",lieu[0],lieu[1],0))
print (valeur_now_num_niveau("arpege-world","PRES","msl",lieu[0],lieu[1],0))
print (valeur_now_num_niveau("arpege-world","GP","agl",lieu[0],lieu[1],0))
print (valeur_now_num_niveau("arpege-world","GP","isobaric",lieu[0],lieu[1],0))
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
      