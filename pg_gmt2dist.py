import sys
import pyproj
#from geotools import *

grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体

point = 0
total = 0
eta = 0
if len(sys.argv) > 1:
    speed = float(sys.argv[1])
else:
#    print("Speed has not input. Use 8.5knot.")
    speed = 5  #knot

line = sys.stdin.readline()
token = [x.strip() for x in line.split(' ')]
lon1, lat1 = token[0], token[1]
if len(token) > 2: speed = token[2]

for line in sys.stdin:
    point = point + 1
    token = [x.strip() for x in line.split(' ')]
    lon2, lat2 = token[0], token[1]

    azimuth, bkw_azimuth, distance = grs80.inv(lon1, lat1, lon2, lat2)
    nauticalmile = distance / 1852
    total = total + nauticalmile
    eta = total / speed

    print('{:03d}'.format(point), '{:6.01f}'.format(azimuth), '{:6.01f}'.format(bkw_azimuth),end="")
    print('{:10.02f}'.format(distance), '{:7.02f}'.format(nauticalmile),'{:10.02f}'.format(total),'{:7.02f}'.format(eta), '{:4.1f}'.format(speed))

    lat1, lon1 = lat2, lon2