from eccodes import *
INPUT= 'AROME_010_SP1_06H_201702040000.grib2'
f = open(INPUT, 'rb')
n=codes_count_in_file (f)
print ("nombre de messages dans le GRIB : ",n)

