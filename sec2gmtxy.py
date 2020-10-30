import sys
from geotools import *

for line in sys.stdin:
    x, y = readxy(line)
    lon, lat = sec2dec(x), sec2dec(y)
    sys.stdout.write("{0} {1}\n".format(lon, lat))