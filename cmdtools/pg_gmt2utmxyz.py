import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    lon, lat, depth = pg.readxyz(line)
    utm_x, utm_y = pg.gmt2utm(lon, lat, +53)
    twt = pg.depth2twt(depth)
    sys.stdout.write("{0} {1} {2}\n".format(utm_x, utm_y, twt))
