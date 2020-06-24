import sys
from geotools import *

for line in sys.stdin:
    utm_x, utm_y = readxy(line)
    lon, lat = utm2gmt(utm_x, utm_y, +53)
    sys.stdout.write("{0} {1}\n".format(lon, lat))
