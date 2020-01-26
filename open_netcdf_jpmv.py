##!usr/bin/env python
#-*- coding:utf-8 -*-

# pour créer le netcdf (dans le shell) :
# sudo apt install libeccodes-tools
# grib_to_netcdf AROME_0.01_SP1_00H_201906300600.grib2 -o test.netcdf

# sudo apt install netcdf-bin
# ncdump -c AROME_0.01_SP1_00H_201906300600.netcdf

import numpy as np
import scipy
import scipy.io
import scipy.io.netcdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cartopy import crs
import cartopy.feature as feature
import cartopy.io.shapereader as shapereader
# get data from the netcdf file
netcdf_data = scipy.io.netcdf.netcdf_file("./test.netcdf", "r")
def getDataFromNetcdf(netcdf_data,key):
    # keys : odict_keys(['longitude', 'latitude', 'time', 'u10', 'v10', 't2m', 'r2'])
    # u10 / v10 => vecteur des vents
    # t2m => température à 2m, c'est stocké comme des entiers, il faut faire un scaling et un offset
    # r2 => humidité à 2m
    print (netcdf_data.variables)
    print (netcdf_data.variables["time"].__dict__)
    print (netcdf_data.variables["time"].data)
    lats  = netcdf_data.variables["latitude"].data
    longs = netcdf_data.variables["longitude"].data
    print (lats,len(lats))
    print (longs,len(longs))
    data = netcdf_data.variables[key].data[0] # 1 grille par pas de temps ?
    if ("scale_factor" in netcdf_data.variables[key].__dict__): # Faut-il scaler les données ?
        scale = netcdf_data.variables[key].scale_factor
        add_offset = netcdf_data.variables[key].add_offset
        print ("scale :",scale,"add_offset :",add_offset)
        data = (data * scale + add_offset)
    print("data : ", key,np.min(data), np.mean(data), np.max(data))
    print (data,len(data))
    XI,YI = np.meshgrid(longs, lats)
    nlat=500
    nlong=500
    print (XI[nlat][nlong],YI[nlat][nlong],data[nlat][nlong])
    nlat=1000
    nlong=1000
    print (XI[nlat][nlong],YI[nlat][nlong],data[nlat][nlong])
    return (XI,YI,data)
(XI,YI,data)=getDataFromNetcdf(netcdf_data,"r2")
# shapefile stuff :
# https://stackoverflow.com/questions/45095681/cartopy-drawing-the-coastlines-with-a-country-border-removed
# https://scitools.org.uk/cartopy/docs/v0.15/tutorials/using_the_shapereader.html
shpfilename=shapereader.natural_earth(resolution='110m',category='cultural',name='admin_0_countries')
countries=shapereader.Reader(shpfilename).geometries()
ax=plt.axes(projection=crs.PlateCarree(central_longitude=90))
ax.add_feature(feature.LAND)
ax.add_feature(feature.OCEAN)
ax.add_geometries(countries,crs.Geodetic(),edgecolor='black',facecolor='none',lw=4)
# ax.coastlines()
graphe = plt.contourf(XI, YI,data,20,transform=crs.PlateCarree(),)
# plt.clabel(graphe,inline=1,fontsize=10,fmt='%3.2f')
plt.colorbar()
plt.savefig("map_temperature.svg",dpi=500) # trick pour exporter en plus grand...
# plt.show()