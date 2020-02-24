from eccodes import *
def toutes_les_valeurs_interpolées(path,lati,longi):
    rep=[]
    f = open(path,'rb')  # ouverture du ficheir Grib
    for i in range (codes_count_in_file(f)):  # boucle sur les Grib contenus dans le fichier
        gid=codes_grib_new_from_file(f)  # chargement en mémoire d grib suivant
        '''
        iterid=codes_keys_iterator_new(gid)
        while codes_keys_iterator_next(iterid):
            keyname = codes_keys_iterator_get_name(iterid)
            keyval = codes_get_string(gid, keyname)
            print("%s = %s" % (keyname, keyval))
        '''
        four=codes_grib_find_nearest(gid,lati,longi,is_lsm=False,npoints=4)  # recherche des 4 points les plus proches
        '''
        print(four,valeur(four))
        for i in range(len(four)):
            print("- %d -" % i)
            print(four[i],codes_get_string(gid,"level"))
        print("-" * 100)
        '''
        rep.append((i,codes_get_string(gid,"level"),valeur_interpolée(four)))
    codes_release(gid)  # libération de la mémoire
    f.close()  # fermeture du fichier Grib
    return (rep)

def valeur_interpolée (four):  # Interpolation linéaire sur les 4 points les plus proches pondérée par l'inverse de la distance
    somme=0.
    somme_des_dist=0.
    for point in four:
        somme=somme+point["value"]/point["distance"]
        somme_des_dist=somme_des_dist+1./point["distance"]
    return (somme/somme_des_dist)

(lati,longi)=(50.6,3.06)
path="arpege-world_20200203_06_WIND_isobaric_9h.grib2"
print(toutes_les_valeurs_interpolées(path,lati,longi))