import sys
#from geotools import *
import pgeotools as pg

lines =  sys.stdin

for l in lines:
    lon, lat = pg.read_dms2xy(l)
    print(lon, lat)