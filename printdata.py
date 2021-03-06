import traceback
import sys

from gribapi import *

#INPUT='AROME_010_SP1_06H_201702040000.grib2'
INPUT='cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2'
VERBOSE=1 # verbose error reporting

def example():
    f = open(INPUT)
    gid = grib_new_from_file(f)

    values = grib_get_values(gid)
   # for i in xrange(len(values)):
   #     print "%d %.10e" % (i+1,values[i])

    print ('%d values found in %s' % (len(values),INPUT))
    print (values[20000])

    for key in ('max','min','average'):
        print ('%s=%.10e' % (key,grib_get(gid,key)))

    grib_release(gid)
    f.close()

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