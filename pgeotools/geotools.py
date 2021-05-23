# geotools for python, for personal work 
# powered by pyproj, pygc
#                         H. Otsuka 2019

import sys, math, re
from pyproj import Proj
from pyproj import Geod
#from pygc import *

#from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

#utm_zone = +53
converter=[]
for utmzone in reversed(range(1,61)):
    converter.append(Proj(proj='utm', zone=utmzone, ellps='WGS84', south='south'))

for utmzone in range(1,61):
    converter.append(Proj(proj='utm', zone=utmzone, ellps='WGS84'))


def great_circle(distance, azimuth, latitude, longitude):
    startLat = latitude
    startLon = longitude
    forwardAzimuth = azimuth
#    distance = dist
    endLon,endLat,backAzimuth = (Geod(ellps='WGS84').fwd(startLon,startLat,forwardAzimuth,distance))

    return {'latitude': endLat,
            'longitude': endLon,
            'reverse_azimuth': backAzimuth}

def rot_xy(x, y, deg):
    rad = math.radians(deg)
    sin_rad = math.sin(rad)
    cos_rad = math.cos(rad)

    rot_x = x * cos_rad - y * sin_rad
    rot_y = x * sin_rad + y * cos_rad

    return rot_x, rot_y

def dms2dec(dms):
    decimal = dms[0] + (dms[1] / 60) + (dms[2] / 3600)
    return decimal

def sec2dec(sec):
    dms = [0,0,0]
    dms[0] = 0
    dms[1] = 0
    dms[2] = sec
    decimal = dms2dec(dms)
    return decimal

def segycoord2(sec):
    #convert segy coordination for unit "2"
    decimal = (sec / 3600000)
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
#    converter = Proj(proj='utm', zone=utm_zone, ellps='WGS84')
#    utm_x, utm_y = converter(lon, lat)
    zone = utm_zone + 60
#     if utm_zone > 0 zone = zone - 1
#    sys.stderr.write(str(zone)+",")
#    sys.stderr.write(str(len(converter))+"\n")
#    conv = converter[zone]
    utm_x, utm_y = converter[zone](lon, lat)
    return utm_x, utm_y

def utm2gmt(utm_x, utm_y, utm_zone):
#    converter = Proj(proj='utm', zone=utm_zone, ellps='WGS84')
#    lon, lat = converter(utm_x, utm_y, inverse=True)
    zone = utm_zone + 60
    lon, lat = converter[zone](utm_x, utm_y, inverse=True)
    return lon, lat

def readsyl(line_in):
    line = line_in.strip()
    token = re.split(',',line)
    sp = int(token[0])
    s_id = str(token[1])
    s_day = str(token[2])
    s_time = str(token[3])
    lon = float(token[4])
    lat = float(token[5])
    return sp, s_id, s_day, s_time, lon, lat

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
        lon0, lat0 = result['longitude'], result['latitude']
        xy = [lon0, lat0]
        xyarray.append(xy)

    return xyarray

def make_mesh_line(lon0, lat0, azm, dist, itr):
    xazm = azm + 90
    lon1, lat1 = lon0, lat0

    iarray = []
    xarray = []

    xy_i = [lon0, lat0]
    xy_x = [lon1, lat1]

    iarray.append(xy_i)
    xarray.append(xy_x)

    for i in range(itr):
        result_i1 = great_circle(distance=dist, azimuth=azm, latitude=lat0, longitude=lon0)
        result_x1 = great_circle(distance=dist, azimuth=xazm, latitude=lat1, longitude=lon1)
        lon0, lat0 = result_i1['longitude'], result_i1['latitude']
        lon1, lat1 = result_x1['longitude'], result_x1['latitude']
        xy_i = [lon0, lat0]
        xy_x = [lon1, lat1]
        iarray.append(xy_i)
        xarray.append(xy_x)

    return iarray, xarray
