
# Voir : https://mf-models-on-aws.org/
import json
import requests
def get_API_jpmv(url):
  r=requests.get(url)
  if r.status_code == 200 : 
      return (json.loads(r.text))
  else :
      print({"http_get_status":r.status_code,"url":url})

for i in range(14):
  heure=8+i
  url="https://61okw3bbmd.execute-api.eu-west-1.amazonaws.com/dev?code_model=arpege-europe&code_param=TMP&code_type_niveau=2m"
  url=url+"&annee=2020&mois=5&jour=6&heure="+str(heure)+"&minute=4&longi=3.06&lati=50.6&liste_de_numniv=1,2,6"
  rep=get_API_jpmv(url)
  print (heure,rep["code_param_unit"]["param_name"],rep["niveaux"])