#
# Copyright 2005-2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
from eccodes import *
INPUT = 'arpege-world_20200203_06_WIND_isobaric_9h.grib2'
f = open(INPUT,'rb')
gid = codes_grib_new_from_file(f)  
iterid = codes_keys_iterator_new(gid)
# Different types of keys can be skipped
# codes_skip_computed(iterid)
# codes_skip_coded(iterid)
# codes_skip_edition_specific(iterid)
# codes_skip_duplicates(iterid)
# codes_skip_read_only(iterid)
# codes_skip_function(iterid)
while codes_keys_iterator_next(iterid):
   keyname = codes_keys_iterator_get_name(iterid)
   #keyval = codes_get_string(gid, keyname)
   print (keyname,": ",end="")
   keyval = codes_get_long_array(gid, keyname)
   print (keyval)
codes_keys_iterator_delete(iterid)
codes_release(gid)
f.close()