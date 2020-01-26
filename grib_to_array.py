
#  https://github.com/difu/gribdb/blob/master/grib_convert/grib2python/grib2array.py

from eccodes import *
missingValue = 1e+20  # A value out of range
def convert_array(input_file):
    all_gribs_structure = []
    f = open(input_file)
    keys = [
        'Ni',
        'Nj',
        'latitudeOfFirstGridPointInDegrees',
        'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees',
        'centre',
        'date'
    ]
    while 1:                                      # boucle sur les messages du fichier
        grib_structure = []
        gid = codes_grib_new_from_file(f)
        if gid is None:
            break
        for key in keys:
            try:
                val = codes_get(gid, key)
                print ('  %s: %s' % (key, val))
                grib_structure.append({key:val})
            except CodesInternalError as err:
                print ('Error with key="%s" : %s' % (key, err.msg))

        print ('There are %d values, average is %f, min is %f, max is %f' % (
            codes_get_size(gid,'values'),
            codes_get(gid,'average'),
            codes_get(gid,'min'),
            codes_get(gid,'max')
        ))
        # Set the value representing the missing value in the field.
        # Choose a missingValue that does not correspond to any real value in the data array
        codes_set(gid,"missingValue",missingValue)
        iterid = codes_grib_iterator_new(gid, 0)
        i = 0
        val_array = []
        while 1:                        # boucle sur les points du message grib
            result = codes_grib_iterator_next(iterid)
            if not result: break
            [lat, lon, value] = result
            val_array.append(value)
            sys.stdout.write("- %d - lat=%.6e lon=%.6e value=" % (i, lat, lon))
            if value == missingValue:
                print ("missing")
            else:
                print ("%.6f" % value)
            i += 1
            if i==300: break
        grib_structure.append({'data':val_array})
        all_gribs_structure.append({'grib':grib_structure})
        codes_grib_iterator_delete(iterid)
        codes_release(gid)
    f.close()
    return all_gribs_structure
    
convert_array("arpege-world_20200113_00_UGRD_agl_42h.grib2")
