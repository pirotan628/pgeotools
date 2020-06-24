import sys
from geotools import *

for line in sys.stdin:
    lon, lat, depth = readxyz(line)
    utm_x, utm_y = gmt2utm(lon, lat, +53)
    twt = depth2twt(depth)
    sys.stdout.write("{0} {1} {2}\n".format(utm_x, utm_y, twt))
