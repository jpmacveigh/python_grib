from gribapi import *


def afficheKeys (gribId,namespace): # iteration sur les key's d'un message
    numKey=1
    iterKeyId = grib_keys_iterator_new(gribId,namespace) # definition d'un iterateur sur les key's
    print "liste des keys pour le namespace : ",namespace
    while 1:   # boucle infinie
        if not grib_keys_iterator_next(iterKeyId): break  # iteration sur les key's
        keyName=grib_keys_iterator_get_name(iterKeyId)  # lecture du nom de la key
        keyVal = grib_get_string(gribId,keyName)     # lecture de la valeur de la key
        keySize=grib_get_size(gribId,keyName)	# lecture de la taille de la key	
        print numKey,"   ",keyName," = ",keyVal, "  keySize : ",keySize
        numKey+=1
    grib_keys_iterator_delete(iterKeyId)
    

def example(path):
    print "nom du fichier GRIB : ",path
    f = open(path,"r")  # ouverture du fichier grib en lecture seule
    print "nb de messages dans le fichier : ",grib_count_in_file(f)
    
    numMessage=1
    keys = ["name","shortName","level","units","date","time","stepRange","validityDate","validityTime","min","max","average"]
    while 1:   # boucle sur les messages du fichier
        messageId = grib_new_from_file(f)
        if messageId is None: break
        print " "
        print "message : ",numMessage,"  longueur : ",grib_get_message_size	(messageId)
        
        for i in range(len(keys)):
            key=keys[i]
            print key," : ",grib_get(messageId,key)
        #print (grib_find_nearest(messageId,50.923,3.0))
        
        #print 'missing value : ',grib_get_double(messageId,"missingValue")
        #afficheKeys(messageId,"ls")   # lecture des keys "ls"
        #afficheKeys(messageId,"parameter")  # lecture des keys "parameter"
        #afficheKeys(messageId,"time")  # lecture des keys "time"
        #afficheKeys(messageId,"geography")  # lecture des keys "geography"
        numMessage += 1
    return
    
    
    i=0
    while 1:
        result = grib_iterator_next(iterId)
        print grib_keys_iterator_get_name(iterId)
        if not result: break
        [lat,lon,value] = result
        if (lat >=50. and lat <=50.1 and lon >=2 and lon <=2.1 ):
            sys.stdout.write("- %d - lat=%.6f lon=%.6f value=" % (i,lat,lon))
            if value == missingValue:
                print "missing"
            else:
                print "%.6f" % value
        i += 1
    grib_iterator_delete(iterId)
    grib_keys_iterator_delete(iterId)
    grib_release(gribId)
    f.close()
#example('AROME_010_SP1_06H_201702040000.grib2')
#example('AROME_0.025_SP1_00H06H_201510131800.grib2')
example('AROME_0.025_SP2_19H24H_201510131800.grib2')