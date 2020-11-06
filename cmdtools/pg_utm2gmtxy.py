import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    utm_x, utm_y = pg.readxy(line)
    lon, lat = pg.utm2gmt(utm_x, utm_y, +53)
    sys.stdout.write("{0} {1}\n".format(lon, lat))
