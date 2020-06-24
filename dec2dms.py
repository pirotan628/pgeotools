import sys
from geotools import *

lines = sys.stdin

for l in lines:
    dmslon, dmslat = read_xy2dms(l)
    dmlon, dmlat = read_xy2dm(l)
    print(dmslon, dmslat,dmlon, dmlat)