# Voir : https://mf-models-on-aws.org/
#INPUT=  "AROME_010_SP1_06H_201702040000.grib2"
#INPUT=  "AROME_0.025_SP1_00H06H_201510131800.grib2"
#INPUT=  "AROME_0.025_SP2_19H24H_201510131800.grib2"
#INPUT = "arpege-world_20200113_00_UGRD_agl_42h.grib2"
#INPUT=  "cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2"
import sys
#sys.path.insert(0,'/home/ubuntu/.local/lib/python3.6/') # insérer dans sys.path le dossier contenant le ou les modules
#sys.path.insert(0,'/home/ubuntu/anaconda3/lib/python3.7/site-packages/') # insérer dans sys.path le dossier contenant le ou les modules

from eccodes import *
print(eccodes.__file__)
import numpy as np
from scipy import interpolate
import datetime
import requests
import json

sys.path.insert(0,'/home/ubuntu/environment/node_jpmv/WCS_MF') # insérer dans sys.path le dossier contenant le ou les modules
from VentHorizontal import VentHorizontal
from VentHorizontal_DDFF import VentHorizontal_DDFF
tempo_grib_file_path="/tmp/tempo.grib2"
les_modeles_MF={      # le pas de temps des sorties de chaque modèle (1 ou 3 heures)
    "arome-france-hd":{"dt-sorties-heures":1},
    "arome-france":{"dt-sorties-heures":1},
    "arpege-europe":{"dt-sorties-heures":1},
    "arpege-world":{"dt-sorties-heures":3}}
    
les_niveaux_possibles=["agl","isobaric","10m","2m","atmosphere","surface","msl","pv"]  # voir : https://mf-models-on-aws.org/

les_param_possibles=[
{"code_param":"ABSV","name_param":"Absolute Vorticity","unit_param":"	s-1","param_accumulation_unit":""},	
{"code_param":"BRTMP","name_param":"Brightness Temperature","unit_param":"K","param_accumulation_unit":""},	
{"code_param":"CAPE","name_param":"Convective Available Potential Energy","unit_param":"J kg-1","param_accumulation_unit":""},	
{"code_param":"CDCC","name_param":"Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"CDCON","name_param":"Convective Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"DLWRF","name_param":"Downward Long-Wave (Thermal) Radiation Flux","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"DLWRFCS","name_param":"Downward Long-Wave (Thermal) Radiation Flux, Clear Sky","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"DPT","name_param":"Dew Point Temperature","unit_param":"K","param_accumulation_unit":""},	
{"code_param":"DSWRF","name_param":"Downward Short-Wave (Solar) Radiation Flux","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"DSWRFCS","name_param":"Downward Short-Wave (Solar) Radiation Flux, Clear Sky","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"DZDT","name_param":"Vertical Velocity (Geometric)","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"EPOT","name_param":"Pseudo-Adiabatic Potential Temperature","unit_param":"K","param_accumulation_unit":""},	
{"code_param":"ETSS","name_param":"Eastward Turbulent Surface Stress","unit_param":"N m-2","param_accumulation_unit":"N m-2 s"},
{"code_param":"EVARATE","name_param":"Evaporation Rate","unit_param":"kg m-2 s-1","param_accumulation_unit":"kg m-2"},
{"code_param":"GP","name_param":"Geopotential","unit_param":"m2 s-2","param_accumulation_unit":""},	
{"code_param":"GPRATE","name_param":"Graupel (Snow Pellets) Prepitation Rate","unit_param":"kg m-2 s-1","param_accumulation_unit":"kg m-2"},
{"code_param":"GUST","name_param":"Wind Speed (Gust)","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"HCDC","name_param":"High Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"HPBL","name_param":"Planetary Boundary Layer Height","unit_param":"m","param_accumulation_unit":""},	
{"code_param":"LCDC","name_param":"Low Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"LHTFL","name_param":"Latent Heat Net Flux","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"MCDC","name_param":"Medium Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"NLWRF","name_param":"Net Long-Wave (Thermal) Radiation Flux","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"NSWRF","name_param":"Net Short-Wave (Solar) Radiation Flux","unit_param":"W m-2","param_accumulation_unit":"J m-2"},
{"code_param":"NTSS","name_param":"Northward Turbulent Surface Stress	N m-2","unit_param":"N m-2 s","param_accumulation_unit":""},
{"code_param":"PRES","name_param":"Pressure","unit_param":"Pa","param_accumulation_unit":""},	
{"code_param":"PVORT","name_param":"Potential Vorticity","unit_param":"K m2","param_accumulation_unit":"kg-1 s-1"},	
{"code_param":"REFZR","name_param":"Equivalent radar reflectivity factor for rain","unit_param":"m m6 m-3","param_accumulation_unit":""},	
{"code_param":"RELV","name_param":"Relative Vorticity","unit_param":"s-1","param_accumulation_unit":""},	
{"code_param":"RH","name_param":"Relative Humidity","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"SCLIWC","name_param":"Specific Cloud Ice Water Content","unit_param":"kg kg-1","param_accumulation_unit":""},	
{"code_param":"SCLLWC","name_param":"Specific Cloud Liquid Water Content","unit_param":"kg kg-1","param_accumulation_unit":""},	
{"code_param":"SHTFL","name_param":"Sensible Heat Net Flux","unit_param":"W m-2","param_accumulation_unit":""},	
{"code_param":"SKINT","name_param":"Skin Temperature","unit_param":"K","param_accumulation_unit":""},	
{"code_param":"SPFH","name_param":"Specific Humidity","unit_param":"kg kg-1","param_accumulation_unit":""},	
{"code_param":"SRAINW","name_param":"Specific Rain Water Content","unit_param":"kg kg-1","param_accumulation_unit":""},	
{"code_param":"SSNOWW","name_param":"Specific Snow Water Content","unit_param":"kg kg-1","param_accumulation_unit":""},	
{"code_param":"TCDC","name_param":"Total Cloud Cover","unit_param":"%","param_accumulation_unit":""},	
{"code_param":"TCWAT","name_param":"Total Column Water","unit_param":"kg m-2","param_accumulation_unit":""},	
{"code_param":"TKE","name_param":"Turbulent Kinetic Energy","unit_param":"J kg-1","param_accumulation_unit":""},	
{"code_param":"TMP","name_param":"Temperature","unit_param":"K","param_accumulation_unit":""},	
{"code_param":"TPRATE","name_param":"Total Precipitation Rate","unit_param":"kg m-2 s-1","param_accumulation_unit":"kg m-2"},
{"code_param":"TSRWE","name_param":"Total Snowfall Rate Water Equivalent","unit_param":"kg m-2 s-1","param_accumulation_unit":"kg m-2"},
{"code_param":"RPRATE","name_param":"Rain Precipitation Rate","unit_param":"kg m-2","param_accumulation_unit":"kg m-2"},
{"code_param":"UGRD","name_param":"U-Component of Wind","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"UGUST","name_param":"U-Component of Wind (Gust)","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"VGRD","name_param":"V-Component of Wind","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"VGUST","name_param":"V-Component of Wind (Gust)","unit_param":"m s-1","param_accumulation_unit":""},	
{"code_param":"VVEL","name_param":"Vertical Velocity (Pressure)","unit_param":"Pa s-1","param_accumulation_unit":""},	
{"code_param":"WDIR","name_param":"Wind Direction (from which blowing)","unit_param":"degrees from North","param_accumulation_unit":""},	
{"code_param":"WIND","name_param":"Wind Speed","unit_param":"m s-1","param_accumulation_unit":""}]	


def assert_code_model(code_model):
    assert code_model in les_modeles_MF.keys() , code_model

def get_param_unit(code_param):
    ''' renvoi l'unité d'un paramètre  ''' 
    for param in les_param_possibles:
        if param["code_param"]==code_param:
            return param["unit_param"]
    return ""

def les_dates_de_sortie_entourant_now_dans_le_temps (code_model):
    now_UTCtimestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())+0.03  # on ajoute 0.03 secondes pour être sur que la date demandée sera future 
    now_UTCdate = datetime.datetime.utcfromtimestamp(now_UTCtimestamp)
    return (les_dates_de_sortie_entourant_date_dans_le_temps(code_model,now_UTCdate))

def les_dates_de_sortie_entourant_date_dans_le_temps (code_model,datetimeUTC):
    ''' calcul les date de sortie d'un model entourant une datetime UTC future '''
    if not(code_model in les_modeles_MF.keys()):
        print ("le code_model est inconnu")
        return (None,"le code_model est inconnu")
    now_UTCtimestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())
    now_UTCdate = datetime.datetime.utcfromtimestamp(now_UTCtimestamp)
    UTCtimestamp = datetime.datetime.timestamp(datetimeUTC)
    if (UTCtimestamp<now_UTCtimestamp):
        print ("la date fournie doitêtre future")
        return(None,"la date fournie n'est pas future")
    date_to_load=get_date_to_load()  # date du dernier run actuel
    i=0
    date=date_to_load
    while (i in range(600)) and (date<datetimeUTC) :
        date=date+datetime.timedelta(hours=les_modeles_MF[code_model]["dt-sorties-heures"])
        i=i+1
    date_before=date-datetime.timedelta(hours=les_modeles_MF[code_model]["dt-sorties-heures"])
    echeance_before=(i-1)*les_modeles_MF[code_model]["dt-sorties-heures"]
    date_after=date
    date_before_timestamp=datetime.datetime.timestamp(date_before)
    date_after_timestamp=datetime.datetime.timestamp(date_after)
    echeance_after=echeance_before+les_modeles_MF[code_model]["dt-sorties-heures"]
    prop=(UTCtimestamp-date_before_timestamp)/(date_after_timestamp-date_before_timestamp)
    return(date_to_load,date_before,echeance_before,date_after,echeance_after,prop)

def get_entourants_grib_messages (code_model,code_param,code_type_niv):    
    assert_code_model(code_model)
    (date_to_load,_,echeance_before,_,echeance_after,prop)=les_dates_de_sortie_entourant_now_dans_le_temps(code_model)
    url_before = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_before)
    url_after  = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_after)
    return (date_to_load,get_grib_messages_from_url(url_before),get_grib_messages_from_url(url_after),prop)

def get_grib_messages (code_model,code_param,code_type_niv,echeance):
    url=get_grib_url_to_load(code_model,code_param,code_type_niv,echeance)
    #print (url)
    return(get_grib_messages_from_url(url))

def get_une_valeur_brute (code_model,code_param,code_type_niv,echeance,rang_message,rang_valeur):
    grib_messages=get_grib_messages (code_model,code_param,code_type_niv,echeance)
    return (grib_messages[rang_message]["values"][rang_valeur])

def get_near_valeurs (code_model,code_param,datepreviUTC,longi,lati):
    ''' Retourne les toutes les valeurs sur la verticale en un point le plus proche d'une date future et d'un position données.
        Toutes les coordonnées verticales disponibles sont retournées.
        Aucune interoplation spatio-temporelle n'est réalisée.
        Au retour, la longueur différente de 0 du paramètre "niveaux" de la réponse doit être testée '''
    res={}
    res["niveaux"]=[]
    now_UTCtimestamp = datetime.datetime.timestamp(datetime.datetime.utcnow())
    now_UTCdate = datetime.datetime.utcfromtimestamp(now_UTCtimestamp)
    res["datenowUTC"]=str(now_UTCdate)
    res["code_modele"]=code_model
    res["code_param"]=code_param
    res["code_param_unit"]=get_param_unit(code_param)
    res["lati_demandee"]=lati
    res["longi_demandee"]=longi
    datepreviUTC_demandee=datepreviUTC
    res["datepreviUTC_demandee"]=str(datepreviUTC_demandee)
    les_dates=les_dates_de_sortie_entourant_date_dans_le_temps (code_model,datepreviUTC)
    if les_dates[0] :
        res["erreur"]=""
        daterunUTC=les_dates[0]
        res["daterunUTC"]=str(daterunUTC)
        prop=les_dates[5]
        if prop >= .5:
            echeance=les_dates[4]
            datepreviUTC=les_dates[3]
        else:
            echeance=les_dates[2]
            datepreviUTC=les_dates[1]
        res["datepreviUTC_trouvee"]=str(datepreviUTC)
        res["echeance"]=echeance
        res["ecart_time(s)"]=datepreviUTC.timestamp()-datepreviUTC_demandee.timestamp()
        rep=(get_profil_vertical(code_model,code_param,echeance,longi,lati))
        niveaux=[]
        for type_niv in rep:
            for niv in type_niv:
                niveaux.append(niv)
        niveaux_alleges=[]
        for niv in niveaux:
            res["longi_trouvee"]=niv[2]
            res["lati_trouvee"]=niv[3]
            res["ecart_distance(km)"]=niv[4]
            nav=[niv[i] for i in range(len(niv)) if (not ((i==2 or i==3 or i==4)))]
            niveaux_alleges.append(nav)
        res["niveaux"]=niveaux_alleges
    else :
        res["status"]=les_dates[1]
    return (res)

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
    (h18,h00,h06,h12)=(4,10,16,22)  # heures UTC avant lesquelles on choisi le réseau correspondant
    if (now_UTChour < h18):
        heure=18
        hier=today-datetime.timedelta(days=1)
        jour=hier
    elif (h18-1 < now_UTChour < h00):
        heure=0
    elif (h00-1 < now_UTChour < h06):
        heure=6
    elif (h06-1 < now_UTChour < h12):
        heure=12
    else:
        heure=18
    return (jour+datetime.timedelta(hours=heure))
    
def get_grib_messages_from_url(url):
    #print (url)
    messages=[]
    res=get_grib_file_from_url(url)
    if (res["http_get_status"]==200) :
        grib=GribFile(tempo_grib_file_path)
        #print ('Type de "grib":',type(grib))
        check=False
        for i in range(len(grib)):
            msg=GribMessage(grib)
            #print ('Type de "msg" : ',type(msg))
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
            construct_times(msg)  # Controle et ajout des dates, heures et echeance du message GRIB 
            messages.append(msg)
    return ({"http_get_status":res["http_get_status"],"messages":messages})


def construct_times(msg):  # calcul et test un paramètre "date_previ" 
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
        return (date_run,echeance,date_previ)
def get_grib_file_from_url(url): # requete l'url sur OpenDataMeteo et met le résultat dans le ficheir tempo_grib_file_path
    #print (url)
    fichier = open(tempo_grib_file_path, "wb")
    r=requests.get(url)
    if r.status_code != 200 : 
        fichier.close()
        return({"http_get_status":r.status_code,"url":url})
    else :
        fichier.write(r.content)
        fichier.close()
        return({"http_get_status":r.status_code,"url":url})

def valeur_now_num_niveau (code_model,code_param,code_type_niv,longitude,latitude,num_niveau):
    (date_to_load,grib_messages_avant,grib_messages_apres,prop)=get_entourants_grib_messages(code_model,code_param,code_type_niv)
    # on traite pour le moment premier niveau et on n'utilise pas l'argument "niveau" TODO
    message_avant=grib_messages_avant[num_niveau]
    message_apres=grib_messages_apres[num_niveau]
    val_avant=value(message_avant,longitude,latitude)
    val_apres=value(message_apres,longitude,latitude)
    valeur_now= (val_avant*(1-prop)+prop*val_apres)
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
    if not ("interpolateur" in msg_grib) :
        les_longitudes=np.array(msg_grib["distinctLongitudes"])
        les_latitudes=np.array(msg_grib["distinctLatitudes"])
        valeurs_sur_la_grille=np.reshape(msg_grib["values"],(msg_grib["Ni"],msg_grib["Nj"]),order="F")
        func=interpolate.interp2d(les_latitudes,les_longitudes,valeurs_sur_la_grille)
        msg_grib.interpolateur=func
    return (msg_grib.interpolateur(latitude,longitude_360(longitude))[0])

def longitude_360(longitude):  # transforme une longitude dans [-180,180] en une dans [0,360]
        assert -180.<=longitude<=180. , longitude
        return ((longitude+360.)%360.)


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
    if code_model == "arome-france-hd":
        print("Données indisponibles avec modèle arome-france-hd")
        return ({})
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

def get_now_profil_vertical_old (code_model,code_param,longitude,latitude):
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
         
def get_now_profil_vertical(code_model,code_param,longitude,latitude):
    assert -180.<=longitude<=180. , longitude
    assert -90.<=latitude<=90. , latitude
    les_niveaux_now_disponibles=get_les_niveaux_now_disponibles(code_model,code_param)
    (date_to_load,date_before,echeance_before,date_after,echeance_after,prop)=les_dates_de_sortie_entourant_now_dans_le_temps (code_model)
    reponse_finale=[]
    for code_type_niv in les_niveaux_now_disponibles["les_niveaux_now_disponibles"]:  # boucle sur les type de niveaux disponibles
        url_before = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_before)
        url_after  = get_grib_url_to_load(code_model,code_param,code_type_niv,echeance_after)
        les_url=(url_before,url_after)
        reponse=[]
        reponse.append(code_type_niv)
        for url in les_url:  # boucle sur les deux échéances entourant "now"
            rep=[]
            get_grib_file_from_url(url)
            f = open(tempo_grib_file_path,'rb')  # ouverture du ficheir Grib
            for i in range (codes_count_in_file(f)):  # boucle sur les Grib contenus dans le fichier
                gid=codes_grib_new_from_file(f)  # chargement en mémoire d grib suivant
                def affiche_Grib_codes():
                    iterid=codes_keys_iterator_new(gid)
                    while codes_keys_iterator_next(iterid):
                        keyname = codes_keys_iterator_get_name(iterid)
                        keyval = codes_get_string(gid, keyname)
                        print("%s = %s" % (keyname, keyval))
                    return()
                #affiche_Grib_codes()
                #exit()
                four=codes_grib_find_nearest(gid,latitude,longitude_360(longitude),is_lsm=False,npoints=4)  # recherche des 4 points les plus proches
                '''
                print(four,valeur(four))
                for i in range(len(four)):
                    print("- %d -" % i)
                    print(four[i],codes_get_string(gid,"level"))
                print("-" * 100)
                '''
                rep.append((i,codes_get_string(gid,"level"),valeur_interpolée_horizontalement(four)))
                codes_release(gid)  # libération de la mémoire
            f.close()  # fermeture du fichier Grib
            reponse.append(rep)
        reponse_now=[]
        code_niv=reponse[0]
        for i in range(len(rep)):
            (_,niv_before,valeur_before)=reponse[1][i]
            (_,niv_after,valeur_after)=reponse[2][i]
            assert niv_before==niv_after
            valeur_now= (valeur_before*(1-prop)+prop*valeur_after)  # interpolation temporelle entre "before" et "after"
            reponse_now.append((i,code_niv,niv_before,code_param,longitude,latitude,valeur_now))
        reponse_finale.append(reponse_now)
        #print(reponse) 
    return (reponse_finale)

def get_profil_vertical(code_model,code_param,echeance,longitude,latitude):
    assert -180.<=longitude<=180. , longitude
    assert -90.<=latitude<=90. , latitude
    les_niveaux_now_disponibles=get_les_niveaux_now_disponibles(code_model,code_param)
    reponse_finale=[]
    for code_type_niv in les_niveaux_now_disponibles["les_niveaux_now_disponibles"]:  # boucle sur les type de niveaux disponibles
        reponse=[]
        reponse.append(code_type_niv)
        rep=[]
        url=get_grib_url_to_load(code_model,code_param,code_type_niv,echeance)
        print(url)
        get_grib_file_from_url(url)
        f = open(tempo_grib_file_path,'rb')  # ouverture du fichier Grib
        for i in range (codes_count_in_file(f)):  # boucle sur les Grib contenus dans le fichier
            gid=codes_grib_new_from_file(f)  # chargement en mémoire du grib suivant
            def affiche_Grib_codes():
                iterid=codes_keys_iterator_new(gid)
                while codes_keys_iterator_next(iterid):
                    keyname = codes_keys_iterator_get_name(iterid)
                    keyval = codes_get_string(gid, keyname)
                    print("%s = %s" % (keyname, keyval))
                return()
            #affiche_Grib_codes()
            #exit()
            le_plus_proche=codes_grib_find_nearest(gid,latitude,longitude_360(longitude),is_lsm=False,npoints=1)  # recherche des 4 points les plus proches
            #print(le_plus_proche)
            rep.append((i,codes_get_string(gid,"level"),le_plus_proche[0]["value"]))
            codes_release(gid)  # libération de la mémoire
        f.close()  # fermeture du fichier Grib
        reponse.append(rep)
        reponse_now=[]
        code_niv=reponse[0]
        for i in range(len(rep)):
            (_,niv,valeur)=reponse[1][i]
            reponse_now.append((code_niv,niv,le_plus_proche[0]["lon"],le_plus_proche[0]["lat"],le_plus_proche[0]["distance"],valeur))
        reponse_finale.append(reponse_now)
    return (reponse_finale)


def valeur_interpolée_horizontalement (four):  # Interpolation linéaire sur les 4 points les plus proches, pondérée par l'inverse de leur distance
    somme=0.
    somme_des_dist=0.
    for point in four:
        if (point["distance"]==0.):  # si on est localisé en un des 4 points, on renvoit la valeur en ce point
            return(point["value"])
        somme=somme+point["value"]/point["distance"]
        somme_des_dist=somme_des_dist+1./point["distance"]
    return (somme/somme_des_dist)

def get_now_profil_vertical_complet(code_model,code_param,longitude,latitude):
    #get_now_profil_vertical_old(code_model,"WIND",lieu[0],lieu[1])
    profil_z=[]
    rep=get_now_profil_vertical(code_model,code_param,longitude,latitude)
    for tab in rep:
        for tob in tab:
            profil_z.append((tob[1],tob[2],tob[6]))
            #print(tob)
    #for i in range(len(profil_z)):
        #print (i, profil_z[i])
    rep=get_now_profil_vertical(code_model,"GP",longitude,latitude)  # acquiqition du profil vertical de géopotentiel
    profil_p={}
    for tab in rep:
        for tob in tab:
            if (tob[1]=="isobaric"):
                profil_p[tob[2]]=tob[6]
            #print(tob)
    for i in range(len(profil_z)):
        if (profil_z[i][0]=="isobaric"):
            if profil_z[i][1] in profil_p :
                profil_z[i]=('agl_from_gp',profil_p[profil_z[i][1]]/10.,profil_z[i][2]) # on divise par 10 pour avoir une hauteur en mètres
            else:
                assert False, ("la pression ",profil_z[i][1]," est absente dans GP")
        else :
            profil_z[i]=(profil_z[i][0],float(profil_z[i][1]),profil_z[i][2])
        #print (i,profil_z[i])    
        
    profil_z=sorted(profil_z, key=lambda x: x[1])  # tri du profil vertical sur les hauteurs "agl" croissantes
    #for i in range(len(profil_z)):
     #   print (i, profil_z[i])
    #print (profil_z)
    return (profil_z)  
 
def get_now_profil_vent_horizontal(code_model,longitude,latitude):
    profil_vertical_direction=get_now_profil_vertical_complet(code_model,"WDIR",longitude,latitude)
    profil_vertical_force=get_now_profil_vertical_complet(code_model,"WIND",longitude,latitude)
    assert len(profil_vertical_direction)==len(profil_vertical_force), (len(profil_vertical_direction),len(profil_vertical_force))
    rep=[]
    for i in range(len(profil_vertical_direction)):
        rep.append((profil_vertical_direction[i][1],profil_vertical_direction[i][2],profil_vertical_force[i][2]))
    return (rep)

def get_now_vent_horizontal (code_model,longitude,latitude,altitude):
    assert altitude >=0,("altitude négative ", latitude)
    profil=get_now_profil_vent_horizontal(code_model,longitude,latitude)
    z=np.array([])
    u=np.array([])
    v=np.array([])
    for i in range(len(profil)):
        z=np.append(z,profil[i][0])
        vent=VentHorizontal_DDFF(profil[i][1],profil[i][2])
        u=np.append(u,vent.u)
        v=np.append(v,vent.v)
    u_z=np.interp(altitude,z,u,left=None,right=None)
    v_z=np.interp(altitude,z,v,left=None,right=None)
    return (u_z,v_z,VentHorizontal(u_z,v_z))
    
def get_now_vent_arpege_world (longitude,latitude,altitude):
  vent=get_now_vent_horizontal("arpege-world",longitude, latitude, altitude)
  return((vent[0],vent[1]))
    
 