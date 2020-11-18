import sys
import pgeotools as pg

lines =  sys.stdin

for l in lines:
    lon, lat = pg.read_dm2xy(l)
    print(lon, lat)