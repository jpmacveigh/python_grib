from __future__ import print_function
import traceback
import sys

 
from gribapi import *
#from eccodes import *

 
#INPUT = 'AROME_0.025_SP1_00H06H_201510131800.grib2'
#INPUT = 'AROME_0.025_SP2_19H24H_201510131800.grib2'
#INPUT='cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2'
INPUT = 'AROME_010_SP1_06H_201702040000.grib2'
VERBOSE = 1  # verbose error reporting
 
 
def example():
    with open(INPUT,"r") as f:
 
        count = grib_count_in_file(f)
        print ("nb de Grib dans le fichier : ",count)
        keys = [
            'parameterName',
            'Ni',
            'Nj',
            #'latitudeOfFirstGridPointInDegrees',
            #'longitudeOfFirstGridPointInDegrees',
            #'latitudeOfLastGridPointInDegrees',
            #'longitudeOfLastGridPointInDegrees',
            ]
 
        i=1
        while 1:
            gid = grib_new_from_file(f)
            if gid is None:
                break
            print ("******** Grib Id : ",i,"   ********")
            for key in keys:
                if not grib_is_defined(gid, key):
                    raise ValueError("Key '%s' was not defined" % key)
                print('%s=%s' % (key, grib_get(gid, key)))
 
            print('There are %d values, average is %f, min is %f, max is %f'
                  % (grib_get_size(gid, 'values'),
                     grib_get(gid, 'average'),
                     grib_get(gid, 'min'),
                     grib_get(gid, 'max')))
            print (grib_find_nearest(gid,50.923,3.0))
            grib_release(gid)
            i=i+1
 
 
def main():
    try:
        example()
    except GribInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print(err.msg, file=sys.stderr)
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())