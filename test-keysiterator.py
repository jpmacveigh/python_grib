import sys
from gribapi import *

infile = 'AROME_0.025_SP1_00H06H_201510131800.grib2'
fid = open(infile,"r")
count = grib_count_in_file(fid)
print ("nb de messages dans le Grib : ",count)
for i in range(count):
   gid = grib_new_from_file(fid)
   iterid = grib_keys_iterator_new(gid)
   keyname="parameterName"
   keyval = grib_get_string(iterid,keyname)
   keytype = grib_get_native_type(gid,keyname)
   print "%d  %s = %s (%s)" % (i,keyname,keyval,str(keytype))

#    grib_skip_computed(iterid)
#    grib_skip_coded(iterid)
#    grib_skip_edition_specific(iterid)
#    grib_skip_duplicated(iterid)
#    grib_skip_read_only(iterid)
#    grib_skip_function(iterid)
   while grib_keys_iterator_next(iterid):
        keyname = grib_keys_iterator_get_name(iterid)
        keyval = grib_get_string(iterid,keyname)
        keytype = grib_get_native_type(gid,keyname)
        print "%s = %s (%s)" % (keyname,keyval,str(keytype)) 
   grib_keys_iterator_delete(iterid)
   grib_release(gid)
fid.close()