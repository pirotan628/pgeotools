import sys
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def dec2dms(dec):
    d = math.floor(dec)
    m = math.floor((dec - d) * 60)
#    s = Decimal(str((dec - d  - (m/60)) * 3600)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    s = round((dec - d  - (m/60)) * 3600, 3)
    dms = [d,m,s]
    return dms

#lon, lat = 135.00833333333333, 34.3555
lines = sys.stdin

for l in lines:
    line = l.strip()
    token = [x.strip() for x in line.split(' ')]
#    print(token)
    if len(token) > 1:
        lon, lat = float(token[0]), float(token[1])
        dlon, dlat = dec2dms(lon), dec2dms(lat)
        print(dlon, dlat)
    else:
        print(line)
