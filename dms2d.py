import sys
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def dms2d(dms):
    decimal = dms[0] + (dms[1] / 60) + (dms[2] / 3600)
    return decimal

lines = sys.stdin

#lon0, lat0 = [135, 8, 0], [34, 27, 30]
#lon, lat = dms2d(lon0), dms2d(lat0)

#print(lon,lat)

for l in lines:
    line = l.strip()
    token = [x.strip() for x in line.split(' ')]
#    print(token)
    if len(token) > 1:
        lat0 = [float(token[0]), float(token[1]), float(token[2])]
        lon0 = [float(token[3]), float(token[4]), float(token[5])]
        lon, lat = dms2d(lon0), dms2d(lat0)
        print(lon, lat)
    else:
        print(line)