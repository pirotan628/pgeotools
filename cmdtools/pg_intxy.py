import sys
#from geotools import *
import pgeotools as pg

for line in sys.stdin:
    fx, fy = pg.readxy(line)
    ix, iy = int(fx), int(fy)
    sys.stdout.write("{0:10d} {1:10d}\n".format(ix, iy))