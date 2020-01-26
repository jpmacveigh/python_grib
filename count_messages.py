import traceback
import sys
 
from gribapi import *
#INPUT='AROME_0.025_SP1_00H06H_201510131800.grib2'
#INPUT='AROME_0.025_SP2_19H24H_201510131800.grib2'
INPUT='cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2'
INPUT="AROME_0.025_SP1_00H06H_201510131800.grib2"
#INPUT='AROME_010_SP1_06H_2017-05-07T18-00-00Z.grib2'
VERBOSE=1 # verbose error reporting

def example():
    f = open(INPUT,"r")
    print ("INPUT :",INPUT)
    mcount = grib_count_in_file(f)
    print ("mcount : ",mcount)
    gid_list = [grib_new_from_file(f) for i in range(mcount)]
    print (gid_list)
    f.close()
    keys = [
        'Ni',
        'Nj',
        'latitudeOfFirstGridPointInDegrees',
        'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees',
        'jDirectionIncrementInDegrees',
        'iDirectionIncrementInDegrees',]
    keys2 = ["name","shortName","level","units","date","time","stepRange","validityDate","validityTime","min","max","average"]

    for i in range(mcount):
        gid = gid_list[i]
        print ("processing message number",i+1)
        iterid = grib_keys_iterator_new(gid,'ls')
        print (iterid)
        keyname = grib_keys_iterator_get_name(iterid)
        print (keyname)
        for key in keys:
            print (key," :",grib_get(gid,key))
        for key in keys2:
            print (key," :",grib_get(gid,key))
        print ('There are %d values, average is %g, min is %g, max is %g' % (
                  grib_get_size(gid,'values'),
                  grib_get(gid,'average'),
                  grib_get(gid,'min'),
                  grib_get(gid,'max') ))
        print ('-'*100)
        grib_release(gid)
def main():
    try:
        example()
    except (GribInternalError,err):
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())