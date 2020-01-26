import traceback
import sys
 
from gribapi import *
 
VERBOSE = 1  # verbose error reporting
 
 
def example(INPUT):
    f = open(INPUT)
    mcount = grib_count_in_file(f)
    print ("nb de messages dans le fichier :",mcount)
    keys2 = ["name","shortName","level","units","date","time","stepRange","validityDate","validityTime","min","max","average"]
    nb=1
    while 1:  # iteration sur les messsages
        gid = grib_new_from_file(f)
        if gid is None:
            break
        print (50*"*")
        print "message : ",nb
        for key in keys2:
            print key," :",grib_get(gid,key)
        iterid = grib_iterator_new(gid, 0)
        bitmapPresent = grib_get(gid, 'bitmapPresent')
        if bitmapPresent:
            # Get the bitmap array which contains 0s and 1s
            bitmap = grib_get_array(gid, 'bitmap', int)
            # Do some sanity checking
            assert len(bitmap) == grib_get_size(gid, 'values')
            assert len(bitmap) == grib_get(gid, 'numberOfDataPoints')
        i = 0
        while 1:
            result = grib_iterator_next(iterid)  # iteration sur les positions
            if not result:
                break
            [lat, lon, value] = result
            if (lat>=50.)and(lat<=50.1)and(lon>=3.)and(lon<=3.1): # test sur la position
                sys.stdout.write("- %d - lat=%.6e lon=%.6e value=" % (i, lat, lon))
                 # Consult bitmap to see if the i'th value is missing
                if bitmapPresent and bitmap[i] == 0:
                    print "missing"
                else:
                    print "%.6f" % value
            i += 1
        grib_iterator_delete(iterid)
        grib_release(gid)
    nb=nb+1
    f.close()
def main():
    try:
        example("AROME_010_SP1_06H_2017-05-07T18-00-00Z.grib2")
    except GribInternalError, err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr, err.msg
        return 1
 
if __name__ == "__main__":
    sys.exit(main())