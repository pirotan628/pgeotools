import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    lon, lat = pg.readxy(line)
    utm_x, utm_y = pg.gmt2utm(lon, lat, +53)
    sys.stdout.write("{0:9.1f} {1:9.1f}\n".format(utm_x, utm_y))
