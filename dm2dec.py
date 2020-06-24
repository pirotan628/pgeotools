import sys
from geotools import *

lines =  sys.stdin

for l in lines:
    lon, lat = read_dm2xy(l)
    print(lon, lat)