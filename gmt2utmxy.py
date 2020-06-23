import sys
import csv
from pyproj import Proj
converter = Proj(proj='utm', zone=53, ellps='WGS84')

for line in sys.stdin:
#   print("--> " + line)
    token = line.split("\t")
    lon = token[0]
    lat = token[1]
#   depth = token[2]
    utm_x, utm_y = converter(lon, lat)
#    twt = 1000 * abs(2 * float(depth)) / 1500
    sys.stdout.write("{0} {1}\n".format(utm_x, utm_y))
#    sys.stdout.write("{0} {1} {2}\n".format(utm_x, utm_y, twt))
