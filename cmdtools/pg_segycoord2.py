import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    x, y = pg.readxy(line)
    lon, lat = pg.segycoord2(x), pg.segycoord2(y)
    sys.stdout.write("{0} {1}\n".format(lon, lat))