from pygc import *

mile = 1852

def dms2d(dms):
    decimal = dms[0] + (dms[1] / 60) + (dms[2] / 3600)
    return decimal

#canter
#lon0, lat0 = 135.1167, 34.5833
#azm = 195.0029
#temp_west
#lon0, lat0 = 135.0333, 34.5000
#azm = 15
#temp_east
#lon0, lat0 = 135.1333, 34.4667
#azm = 15
#West
#lon0, lat0 = 135.06463644790844, 34.59675532370867
#azm = 195.0029
#East
#lon0, lat0 = 135.16462397177628, 34.56345585306766
#azm = 195.0029
#cross-lines
#lon0, lat0 = 134.9667, 34.3000
#lon0, lat0 = 135.0500, 34.3167
#135:03, 34:34

#plan_S
#lon0, lat0 = 135.05, 34.5667
#135:12, 34:31
#lon0, lat0 = 135.2000, 34.5167

#Sumoto-oki-point
#135:00:30, 34:21:19.8
#lon0,lat0 = dms2d([135,0,30]), dms2d([34,21,19.8])
#lon0, lat0 = 135.03440954334428, 34.43612923471752 # North Center
lon0, lat0 = 134.9953139534642, 34.31518290300008  # South Center

azm, dist, itr = 90, -0.1 * mile, 30


#azm = 15
#azm = 195.0029
#azm = 90
#azm = 270

#dist = 0.1 * mile
#itr = 10

#print( "{0} {1} {2}".format(lon0,lat0,0))
print("{0} {1}".format(lon0,lat0))
for i in range(itr):
    result = great_circle(distance=dist, azimuth=azm, latitude=lat0, longitude=lon0)
#    print( "{0} {1} {2}".format(result['longitude'],result['latitude'],result['reverse_azimuth']))
    print( "{0} {1}".format(result['longitude'],result['latitude']))
    lon0, lat0 = result['longitude'], result['latitude']
