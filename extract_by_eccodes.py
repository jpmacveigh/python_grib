#
# Voir : https://mf-models-on-aws.org/
# 
import json
import datetime 
import sys
sys.path.append("/opt/")
#sys.path.append("/opt/python/gribapi/")
#from gribapi import *
from eccodes import *
from util_eccodes import *
def main(event,context):
    query_string=event["queryStringParameters"]
    code_modele=query_string["code_model"]             # code du modèle demandé
    code_param=query_string["code_param"]              # code du paramètre demandé
    code_type_niveau=query_string["code_type_niveau"]  # code du type de niveaux demandés
    annee =int(query_string["annee"])    # date de la prévision demandée. Le run utilisé sera le plus récent
    mois  =int(query_string["mois"])
    jour  =int(query_string["jour"])
    heure =int(query_string["heure"])
    minute=int(query_string["minute"])
    lati=float(query_string["lati"])              # latiude de la position demanée 
    longi=float(query_string["longi"])            # longitude de la position demandée
    if "liste_de_numniv" in query_string:
      liste_de_numniv=query_string["liste_de_numniv"]    # liste des numéros de niveau demandés (numérotés à partir de 1)
      liste=liste_de_numniv.split(",")
      liste_de_numniv=[int(i) for i in liste]
    else : liste_de_numniv=None
    datepreviUTC=datetime.datetime(annee,mois,jour,heure,minute)
    rep=extract_liste_de_niveaux(code_modele,code_param,code_type_niveau,datepreviUTC,lati,longi,liste_de_numniv)
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(rep)
    }
context=""
event={
  "queryStringParameters": {
    "code_model": "arpege-europe",
    "code_param": "TMP",
    "code_type_niveau": "isobaric",
    "annee":"2020",
    "mois":"05",
    "jour":"05",
    "heure":"15",
    "minute":"06",
    "lati": "50.6",
    "longi": "3.06",
    "liste_de_numniv": "1,20,21,65580,22"
  }
}
rep=main (event,context)



