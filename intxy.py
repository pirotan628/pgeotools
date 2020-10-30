import sys
from geotools import *

for line in sys.stdin:
    fx, fy = readxy(line)
    ix, iy = int(fx), int(fy)
    sys.stdout.write("{0:10d} {1:10d}\n".format(ix, iy))