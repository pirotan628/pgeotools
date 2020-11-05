import sys
from geotools import *

for line in sys.stdin:
    x, y = readxy(line)
    lon, lat = segycoord2(x), segycoord2(y)
    sys.stdout.write("{0} {1}\n".format(lon, lat))