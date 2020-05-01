# A GRIB file handle meant for use in a context manager.
# One can easily iterate over each message in the file::
from eccodes import *
filename="arpege-world_20200203_06_WIND_isobaric_9h.grib2"
print(filename)
grib=GribFile(filename)
#print(dir(grib))
print ("nombre de messages dans le fichier GRIB : ",len(grib))  # Print number of messages in file
#print(dir(grib))
messages=[]
for i in range(len(grib)):
  messages.append(grib.next())
#print(dir(messages[0]))
for i in range(1):   #msg in messages:
  msg=messages[i]
  #print(dir(msg))
  #print(msg.keys())
  #print(msg.items())
  #print(msg["level"],msg["values"],msg["latitudes"],msg["longitudes"],msg.items(),msg.keys())
  #val=codes_grib_find_nearest	(msg["grib_index"],50.6,3.06,is_lsm=False,npoints=1)
  #print(val)
  index=GribIndex(filename,"toto") 
  print(index.size)
  print(dir(index))
  print (index.values)
  print (dir(index.values))