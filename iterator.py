import traceback
import sys
 
from gribapi import *
 
INPUT='AROME_010_SP1_06H_201702040000.grib2'
VERBOSE=1 # verbose error reporting
 
def example():
    f = open(INPUT)
    nb=grib_count_in_file(f)
    print "nb de grib dans le fichier : ",nb
    while 1:
        gid = grib_new_from_file(f)
        
        if gid is None: break
 
        iterid = grib_iterator_new(gid,0)
 
        missingValue = grib_get_double(gid,"missingValue")
 
        i=0
        while 1:
            result = grib_iterator_next(iterid)
            if not result: break
 
            [lat,lon,value] = result
 
            if lat >= 50.1 and lat <=50.2 and lon >2.0 and lon <= 2.1 :
                sys.stdout.write("- %d - lat=%.6f lon=%.6f value=" % (i,lat,lon))
     
                if value == missingValue:
                    print "missing"
                else:
                    print "%.6f" % value
     
                i += 1
             
        grib_iterator_delete(iterid)
        grib_release(gid)
 
    f.close()
 
def main():
    try:
        example()
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())