
import traceback
import sys
 
from gribapi import *
 
INPUT='AROME_010_SP1_06H_201702040000.grib2'
VERBOSE=1 # verbose error reporting
 
def example():
    f = open(INPUT)
 
    mcount = grib_count_in_file(f)
    gid_list = [grib_new_from_file(f) for i in range(mcount)]
 
    f.close()
 
    keys = [
        'Ni',
        'Nj',
        'latitudeOfFirstGridPointInDegrees',
        'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees',
        'jDirectionIncrementInDegrees',
        'iDirectionIncrementInDegrees',
        ]
 
    for i in range(mcount):
        gid = gid_list[i]
 
        print ("processing message number",i+1)
 
        for key in keys:
            print ('%s=%g' % (key,grib_get(gid,key)))
 
        print ('There are %d, average is %g, min is %g, max is %g' % (
                  grib_get_size(gid,'values'),
                  grib_get(gid,'average'),
                  grib_get(gid,'min'),
                  grib_get(gid,'max')
               ))
 
        print ('-'*100)
 
        grib_release(gid)
 
 
def main():
    example()
 
if __name__ == "__main__":
    sys.exit(main())