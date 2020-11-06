import sys
#from geotools import *
import pgeotools as pg

lines = sys.stdin

for l in lines:
    dmslon, dmslat = pg.read_xy2dms(l)
    dmlon, dmlat = pg.read_xy2dm(l)
    print(dmslon, dmslat,dmlon, dmlat)
