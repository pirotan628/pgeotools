import sys
from geotools import *

for line in sys.stdin:
    lon, lat = readxy(line)
    utm_x, utm_y = gmt2utm(lon, lat, +53)
    sys.stdout.write("{0} {1}\n".format(utm_x, utm_y))
