import sys
from geotools import *
from segytools import *

tmp_sps = spsfile(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

for line in sys.stdin:
    sp, s_id, s_day, s_time, lon, lat = readsyl(line)
    utm_x, utm_y = gmt2utm(lon, lat, +53)
    dayofyear = datetime.strftime(datetime.strptime(s_day.strip(), '%Y/%m/%d'), '%j')
    hms = datetime.strftime(datetime.strptime(s_time.strip(),'%H:%M:%S.%f'),'%H%M%S')

    tmp_sps.record_identification = "S"
    tmp_sps.point_number = sp
    tmp_sps.line_name = s_id

    tmp_sps.map_grid_easting = utm_x
    tmp_sps.map_grid_northing = utm_y

    tmp_sps.point_index = 1
    tmp_sps.point_code = 0
    tmp_sps.static_correction = 0
    tmp_sps.point_depth = 0
    
    tmp_sps.seismic_datum = 0
    tmp_sps.uphole_time = 0
    tmp_sps.water_depth = 0 
    tmp_sps.surface_elevation = 0

    tmp_sps.day_of_year = int(dayofyear)
    tmp_sps.time_hhmmss = str(hms)

#    print("S%16s%8d%1d%2s%4d%4.1f%4d%2d%4.1f%9.1f%10.1f%6.1f%3d%6s",s_id,sp,point_index,point_code,st_cr,point_depth,seismic_data,uphole_time,wd,utm_x,utm_y,elv,julday,s_time)

    printsps(tmp_sps)

#    sys.stdout.write("S{0:16s}{1:8d}{2:1d}{3:2d}{4:4d}".format(s_id,sp,point_index,point_code,st_cr))
#    sys.stdout.write("{0:4.1f}{1:4d}{2:2d}{3:4.1f}".format(point_depth,seismic_data,uphole_time,wd))
#    sys.stdout.write("{0:9.1f}{1:10.1f}{2:6.1f}{3:3d}{4:6s}\n".format(utm_x,utm_y,elv,julday,s_time))
