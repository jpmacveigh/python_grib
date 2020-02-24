import traceback
import sys
 
from gribapi import *
 
#INPUT='AROME_0.025_SP1_00H06H_201510131800.grib2'
#INPUT='AROME_010_SP1_06H_201702040000.grib2'
INPUT='cosmo-d2_germany_rotated-lat-lon_single-level_2018080818_006_T_2M.grib2'
VERBOSE=1 # verbose error reporting
 
def example():
    grib_multi_support_on()	
    print ("INPUT = ",INPUT)
    f = open(INPUT)
    mcount = grib_count_in_file(f)
    print ("nb de messages dans le fichier : ",mcount)
    nbmessages=0
    while 1:
        gid = grib_new_from_file(f,headers_only=True)		
        if gid is None: break
        nbmessages+=1
        print ("*****************  message : %i" % (nbmessages))
        iterid = grib_keys_iterator_new(gid,'ls')
        # Different types of keys can be skipped
        # grib_skip_computed(iterid)
        # grib_skip_coded(iterid)
        # grib_skip_edition_specific(iterid)
        # grib_skip_duplicates(iterid)
        # grib_skip_read_only(iterid)
        # grib_skip_function(iterid)
        nbkeys=0 
        while grib_keys_iterator_next(iterid):
            keyname = grib_keys_iterator_get_name(iterid)
            keyval = grib_get_string(iterid,keyname)
            nbkeys+=1
            print ("key %i  %s = %s" % (nbkeys,keyname,keyval))
        #grib_keys_iterator_delete(iterid)
        #grib_release(gid)
    #f.close()
def main():
    try:
        example()
    except (GribInternalError,err):
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>(sys.stderr,err.msg)
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())