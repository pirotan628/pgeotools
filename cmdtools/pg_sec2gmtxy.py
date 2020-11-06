import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    x, y = pg.readxy(line)
    lon, lat = pg.sec2dec(x), pg.sec2dec(y)
    sys.stdout.write("{0} {1}\n".format(lon, lat))