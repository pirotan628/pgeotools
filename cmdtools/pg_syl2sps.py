import sys
from datetime import datetime
import pgeotools as pg
from pgeotools import segytools as psg

tmp_sps = psg.spsfile(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

for line in sys.stdin:
    sp, s_id, s_day, s_time, lon, lat = pg.readsyl(line)
    utm_x, utm_y = pg.gmt2utm(lon, lat, +53)
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

    psg.printsps(tmp_sps)
