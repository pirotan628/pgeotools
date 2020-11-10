import sys
import pgeotools as pg
from pg_param import *

utmzone = PROJECT_UTM

for line in sys.stdin:
    lon, lat = pg.readxy(line)
    utm_x, utm_y = pg.gmt2utm(lon, lat, utmzone)
    sys.stdout.write("{0:9.1f} {1:9.1f}\n".format(utm_x, utm_y))
