from eccodes import *
#INPUT=  "AROME_010_SP1_06H_201702040000.grib2"
#INPUT=  "AROME_0.025_SP1_00H06H_201510131800.grib2"
INPUT=  "AROME_0.025_SP2_19H24H_201510131800.grib2"
#INPUT=  "cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2"
with GribFile(INPUT) as grib:
    messages=[]
    for i in range(len(grib)):  # range(0,1)
         msg = GribMessage(grib)
         messages.append(msg)
    print (" ************* Nombre de messages dans le fichier Grib : ",len(messages))
    print (messages[0].keys())
    n=1
    for msg in messages : 
         print (n,msg["name"],msg["level"],msg["date"],msg["hour"],msg["forecastTime"],msg["validityDate"],msg["validityTime"])
         n=n+1
         '''
         for k in msg.keys():
           print (k," : ",msg[k])
         '''