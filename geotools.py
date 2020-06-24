import sys
import math
from pyproj import Proj
from pygc import *
#from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import re

nmile = 1852

def dms2dec(dms):
    decimal = dms[0] + (dms[1] / 60) + (dms[2] / 3600)
    return decimal

def dec2dms(dec):
    d = math.floor(dec)
    m = math.floor((dec - d) * 60)
#    s = Decimal(str((dec - d  - (m/60)) * 3600)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    s = round((dec - d  - (m/60)) * 3600, 3)
    dms = [d,m,s]
    return dms

def dec2dm(dec):
    d = math.floor(dec)
    m = round((dec - d) * 60, 4)
    dm = [d,m]
    return dm

def gmt2utm(lon, lat, utm_zone):
    converter = Proj(proj='utm', zone=utm_zone, ellps='WGS84')
    utm_x, utm_y = converter(lon, lat)
    return utm_x, utm_y

def utm2gmt(utm_x, utm_y, utm_zone):
    converter = Proj(proj='utm', zone=utm_zone, ellps='WGS84')
    lon, lat = converter(utm_x, utm_y, inverse=True)
    return lon, lat

def readxy(line_in):
    line = line_in.strip()
    token = re.split('[\t\s]',line)
    lon = float(token[0])
    lat = float(token[1])
    return lon, lat

def readxyz(line_in):
    line = line_in.strip()
    token = re.split('[\t\s]',line)
    lon = float(token[0])
    lat = float(token[1])
    depth = float(token[2])
    return lon, lat, depth

def read_dms2xy(line_in):
    line = line_in.strip()
    token = [x.strip() for x in re.split('[\t\s]', line)]
    if len(token) > 1:
        lon0 = [float(token[0]), float(token[1]), float(token[2])]
        lat0 = [float(token[3]), float(token[4]), float(token[5])]
        lon, lat = dms2dec(lon0), dms2dec(lat0)
    else:
        return False

    return lon, lat

def read_dm2xy(line_in):
    line = line_in.strip()
    token = [x.strip() for x in re.split('[\t\s]', line)]
    if len(token) > 1:
        lon0 = [float(token[0]), float(token[1]), 0]
        lat0 = [float(token[2]), float(token[3]), 0]
        lon, lat = dms2dec(lon0), dms2dec(lat0)
    else:
        return False

    return lon, lat

def read_xy2dms(line_in):
    line = line_in.strip()
    token = [x.strip() for x in re.split('[\t\s]', line)]
    if len(token) > 1:
        lon, lat = float(token[0]), float(token[1])
        dlon, dlat = dec2dms(lon), dec2dms(lat)
    else:
        return False

    return dlon, dlat

def read_xy2dm(line_in):
    line = line_in.strip()
#    token = [x.strip() for x in line.split(' ')]
    token = [x.strip() for x in re.split('[\t\s]', line)]
    if len(token) > 1:
        lon, lat = float(token[0]), float(token[1])
        dlon, dlat = dec2dm(lon), dec2dm(lat)
    else:
        return False

    return dlon, dlat

def twt2depth(twt):
    depth = abs(twt / 2) * 1.5
    return depth

def depth2twt(depth):
    twt = 1000 * abs(2 * depth) / 1500
    return twt

def make_regular_interval(lon0, lat0, azm, dist, itr):
    xyarray = []
    xy = [lon0, lat0]
    xyarray.append(xy)
    for i in range(itr):
        result = great_circle(distance=dist, azimuth=azm, latitude=lat0, longitude=lon0)
#        print( "{0} {1}".format(result['longitude'],result['latitude']))
        lon0, lat0 = result['longitude'], result['latitude']
        xy = [lon0, lat0]
        xyarray.append(xy)

    return xyarray