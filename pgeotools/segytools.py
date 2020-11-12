# segytools for python, for personal work
# powered by obspy, pyproj
#                           H.Otsuka 2020

import sys, os
import pandas as pd
from datetime import datetime
from obspy.io.segy.core import _read_segy as _read_segy_core
from obspy.io.segy.segy import _read_segy as _read_segy_segy
import pyproj
from pgeotools import geotools
#from pgeotools import param_config as pconf

class config_file:
    def __init__(self,WRKHOME,PATH_RAW,PATH_HDR,PATH_ASC,PATH_WRK,PATH_PRC, \
                EXT_SGY,EXT_SU,EXT_TXT,EXT_BIN,EXT_SPS,EXT_RPS,EXT_XPS, \
                PFX_HDR,PFX_BIN,SFX_):
        self.WRKHOME = WRKHOME
        self.PATH_RAW = PATH_RAW
        self.PATH_HDR = PATH_HDR
        self.PATH_ASC = PATH_ASC
        self.PATH_WRK = PATH_WRK
        self.PATH_PRC = PATH_PRC
        self.EXT_SGY = EXT_SGY
        self.EXT_SU = EXT_SU
        self.EXT_TXT = EXT_TXT
        self.EXT_BIN = EXT_BIN
        self.EXT_SPS = EXT_SPS
        self.EXT_RPS = EXT_RPS
        self.EXT_XPS = EXT_XPS
        self.PFX_HDR = PFX_HDR
        self.PFX_BIN = PFX_BIN
        self.SFX_ = SFX_        

class Sufgrp:
# class for su file group
    def __init__(self, basename, tape, sufile, hfile, bfile):
        self.basename = basename
        self.tape = tape
        self.sufile = sufile
        self.hfile = hfile
        self.bfile = bfile

class spsfile:
    def __init__(self,record_identification,line_name,point_number,point_index,point_code,\
                static_correction,point_depth,seismic_datum,uphole_time,water_depth, \
                map_grid_easting,map_grid_northing,surface_elvation,day_of_year,time_hhmmss):

        self.record_identification = record_identification
        self.line_name = line_name
        self.point_number = point_number           #shot point
        self.point_index = point_index
        self.point_code = point_code
        self.static_correction = static_correction
        self.point_depth = point_depth
        self.seismic_datum = seismic_datum
        self.uphole_time = uphole_time
        self.water_depth = water_depth
        self.map_grid_easting = map_grid_easting   #utm_x
        self.map_grid_northing = map_grid_northing #utm_y
        self.surface_elvation = surface_elvation
        self.day_of_year = day_of_year
        self.time_hhmmss = time_hhmmss

class ship_configuration:
    def __init__(self, gps_to_source_stern, gps_to_source_right, gps_to_receiver_stern, gps_to_receiver_right):
        self.gps_to_source_stern = gps_to_source_stern
        self.gps_to_source_right = gps_to_source_right
        self.gps_to_receiver_stern = gps_to_receiver_stern
        self.gps_to_receiver_right = gps_to_receiver_right

def read_segy(s1):
#        segy = _read_segy_core(s1.tape[i],unpack_trace_headers=True)
#        print(segy.__str__(extended=True))
    return 0

def su_segyread(s1):
    for i in range(len(s1)):
        command = ["segyread", "tape=" + s1[i].tape, "bfile=" + s1[i].bfile, "hfile=" + s1[i].hfile, "> " + s1[i].sufile]
        args = " ".join(command)

        print(args)
        os.system(args)

    return 0

def sps2sugeom(spsfile, config):

    return 0 

def testsu(s1):
    for i in range(len(s1)):

        command = ["sugethw", "key=tracl,fldr,year,day,minute,sec", "< " + s1[i].sufile]
        args = " ".join(command)        
        print(args)
#        os.system(args)

    return 0

def findxy_from_time(reference, timing, latlon, utmzone):
    
    utm_x, utm_y = 0, 0

    selected = pd.DataFrame()
    selected = reference.iloc[reference.index.get_loc(timing, method='nearest')]

    x = float(selected.loc['lat'])
    y = float(selected.loc['lon'])
    
    if latlon == True:
        utm_x, utm_y = geotools.gmt2utm(y, x, utmzone)
    else:
        utm_x, utm_y = x, y

    return utm_x, utm_y


def printsps(sps):
    sys.stdout.write("{0:1s}{1:16s}{2:8d}{3:1d}{4:2d}{5:4d}".format(sps.record_identification,sps.line_name,sps.point_number,sps.point_index,sps.point_code,sps.static_correction))
    sys.stdout.write("{0:4.1f}{1:4d}{2:2d}{3:4.1f}".format(sps.point_depth,sps.seismic_datum,sps.uphole_time,sps.water_depth))
    sys.stdout.write("{0:9.1f}{1:10.1f}{2:6.1f}{3:3d}{4:6s}\n".format(sps.map_grid_easting,sps.map_grid_northing,sps.surface_elvation,sps.day_of_year,sps.time_hhmmss))

    return 0

def create_sps_from_descrete(s1, gpsfile, utmzone):

    gpsdata = pd.DataFrame()
    gpsdata = pd.read_csv(gpsfile,sep=",",names=['date_time','lat','lon'],\
                                       parse_dates=True, header=None)

    gpsdata['date_time'] = pd.to_datetime(gpsdata['date_time'])
    gpsdata.set_index(gpsdata['date_time'],drop=True, inplace=True)
    gpsdata = gpsdata.drop_duplicates(['date_time'])
    gpsdata = gpsdata.sort_index()

    for i in range(len(s1)):
        sps = []
        segy = _read_segy_segy(s1[i].tape)
        for j in range(len(segy.traces)):
#            tr = segy.traces[j]
            hdr = segy.traces[j].header
            if hdr.trace_number_within_the_original_field_record == 1:
                strf = " ".join([str(hdr.year_data_recorded),str(hdr.day_of_year),str(hdr.hour_of_day),str(hdr.minute_of_hour),str(hdr.second_of_minute)])
                timing = datetime.strptime(strf,'%y %j %H %M %S')
                hms = datetime.strftime(timing,'%H%M%S')
                utm_x, utm_y = findxy_from_time(gpsdata, timing, True, utmzone)

                tmp_sps = spsfile(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                tmp_sps.record_identification = "S"
                tmp_sps.line_name = s1[i].basename
                tmp_sps.point_number = hdr.original_field_record_number
                tmp_sps.point_index = 1
                tmp_sps.map_grid_easting = utm_x
                tmp_sps.map_grid_northing = utm_y
                tmp_sps.day_of_year = hdr.day_of_year
                tmp_sps.time_hhmmss = str(hms)
                sps.append(tmp_sps)
#        for k in range(len(sps)):
#            printsps(sps[k])
    return sps

def create_utmxy_from_hdrtime(s1, gpsfile, utmzone):

    gpsdata = pd.DataFrame()
    gpsdata = pd.read_csv(gpsfile,sep=",",names=['date_time','lat','lon'],\
                                       parse_dates=True, header=None)

    gpsdata['date_time'] = pd.to_datetime(gpsdata['date_time'])
    gpsdata.set_index(gpsdata['date_time'],drop=True, inplace=True)
    gpsdata = gpsdata.drop_duplicates(['date_time'])
    gpsdata = gpsdata.sort_index()

    for i in range(len(s1)):
        coordination = []
        segy = _read_segy_segy(s1[i].tape)
        for j in range(len(segy.traces)):
#            tr = segy.traces[j]
            hdr = segy.traces[j].header
#            if hdr.trace_number_within_the_original_field_record == 1:
            strf = " ".join([str(hdr.year_data_recorded),str(hdr.day_of_year),str(hdr.hour_of_day),str(hdr.minute_of_hour),str(hdr.second_of_minute)])
            timing = datetime.strptime(strf,'%y %j %H %M %S')
            #print(timing)
#            hms = datetime.strftime(timing,'%H%M%S')
            utm_x, utm_y = findxy_from_time(gpsdata, timing, True, utmzone)
            utm_xy = [utm_x, utm_y]
            coordination.append(utm_xy)
    return coordination

def makesufgrp(basename, conf_f):
    s1 = []
    for i in range(len(basename)):
        tape = conf_f.WRKHOME + conf_f.PATH_RAW + basename[i] + conf_f.EXT_SGY
        sufile = conf_f.WRKHOME + conf_f.PATH_WRK + basename[i] + conf_f.EXT_SU
        hfile = conf_f.WRKHOME + conf_f.PATH_HDR + conf_f.PFX_HDR + basename[i] + conf_f.EXT_TXT
        bfile = conf_f.WRKHOME + conf_f.PATH_HDR + conf_f.PFX_BIN + basename[i] + conf_f.EXT_BIN
        tmp_strm = Sufgrp(basename[i], tape, sufile, hfile, bfile)
        s1.append(tmp_strm)
#       print(s1[i].tape)
    return s1

def calc_geom_from_ship_conf(ship_conf, gps_pos, utm_zone):
    grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体
    coord = []
    coords = []
    append = coords.append

    sx, sy, gx, gy= 0, 0, 0, 0

    lon0, lat0 = gps_pos[0][0], gps_pos[0][1]
    x0, y0 = geotools.gmt2utm(lon0, lat0, utm_zone)

    sx0 = ship_conf.gps_to_source_right
    sy0 = -1 * ship_conf.gps_to_source_stern
    gx0 = ship_conf.gps_to_receiver_right
    gy0 = -1 * ship_conf.gps_to_receiver_stern

    for itr in range(1,len(gps_pos) - 1):
        lon1, lat1 = gps_pos[itr][0], gps_pos[itr][1]
        x0, y0 = geotools.gmt2utm(lon0, lat0, utm_zone)
        x1, y1 = geotools.gmt2utm(lon1, lat1, utm_zone)
        azimuth, bkw_azimuth, distance = grs80.inv(lon0, lat0, lon1, lat1)
        deg = -1 * azimuth
        rot_sx0, rot_sy0 = geotools.rot_xy(sx0, sy0, deg)
        rot_gx0, rot_gy0 = geotools.rot_xy(gx0, gy0, deg)
        sx = x0 + rot_sx0
        sy = y0 + rot_sy0
        gx = x0 + rot_gx0
        gy = y0 + rot_gy0
#        sx = gps_pos[itr,0] + ship_conf.gps_to_source_stern
#        sy = gps_pos[itr,1] + ship_conf.gps_to_source_right
        coord = [sx,sy,gx,gy,azimuth]
        append(coord)
        lon0, lat0 = lon1, lat1

    sx = x1 + rot_sx0
    sy = y1 + rot_sy0
    gx = x1 + rot_gx0
    gy = y1 + rot_gy0
    coord = [sx,sy,gx,gy,azimuth]
    append(coord)
    
    return coords