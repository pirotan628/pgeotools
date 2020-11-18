import sys
import pgeotools as pg
from pg_param import *

utmzone = PROJECT_UTM

for line in sys.stdin:
    utm_x, utm_y = pg.readxy(line)
    lon, lat = pg.utm2gmt(utm_x, utm_y, utmzone)
    sys.stdout.write("{0} {1}\n".format(lon, lat))
