import sys
from geotools import *

for line in sys.stdin:
    sp, s_id, s_day, s_time, lon, lat = readsyl(line)
    utm_x, utm_y = gmt2utm(lon, lat, +53)

    point_index,point_code,st_cr,point_depth=1,0,0,0
    seismic_data,uphole_time,wd,elv=0,0,0,0
    julday,s_time = 0,"000000"

#    print("S%16s%8d%1d%2s%4d%4.1f%4d%2d%4.1f%9.1f%10.1f%6.1f%3d%6s",s_id,sp,point_index,point_code,st_cr,point_depth,seismic_data,uphole_time,wd,utm_x,utm_y,elv,julday,s_time)

    sys.stdout.write("S{0:16s}{1:8d}{2:1d}{3:2d}{4:4d}".format(s_id,sp,point_index,point_code,st_cr))
    sys.stdout.write("{0:4.1f}{1:4d}{2:2d}{3:4.1f}".format(point_depth,seismic_data,uphole_time,wd))
    sys.stdout.write("{0:9.1f}{1:10.1f}{2:6.1f}{3:3d}{4:6s}\n".format(utm_x,utm_y,elv,julday,s_time))
