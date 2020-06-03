def dms2d(dms):
    decimal = dms[0] + (dms[1] / 60) + (dms[2] / 3600)
    return decimal

lon0, lat0 = [135, 8, 0], [34, 27, 30]
lon, lat = dms2d(lon0), dms2d(lat0)

print(lon,lat)
