#import subprocess
#import sys
import pandas as pd
from datetime import datetime
import os
from obspy.io.segy.core import _read_segy as _read_segy_core
from obspy.io.segy.segy import _read_segy as _read_segy_segy
from geotools import *


WRKHOME = '../'

#PATH_RAW = 'rawdata'
PATH_RAW = '../202006_Onokoro/'
PATH_HDR = 'headers/'
PATH_ASC = 'ascdata/'
PATH_WRK = 'working/'
PATH_PRC = 'processed/'

EXT_SGY = '.sgy'
EXT_SU = '.su'
EXT_TXT = '.txt'
EXT_BIN = '.bin'
EXT_SPS = '.sps'

PFX_HDR = 'hdr_'
PFX_BIN = 'bin_'
SFX_ = ''

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

def read_segy(s1):
#        segy = _read_segy_core(s1.tape[i],unpack_trace_headers=True)
#        print(segy.__str__(extended=True))
    for i in range(len(s1)):
        command = ["segyread", "tape=" + s1[i].tape, "bfile=" + s1[i].bfile, "hfile=" + s1[i].hfile, "> " + s1[i].sufile]
        args = " ".join(command)

        print(args)
        os.system(args)

    return 0

def sps2geom(spsfile):

    return 0 

def testsu(s1):
    for i in range(len(s1)):

        command = ["sugethw", "key=tracl,fldr,year,day,minute,sec", "< " + s1[i].sufile]
        args = " ".join(command)        
        print(args)
#        os.system(args)

    return 0

def findxy_from_time(reference, timing, latlon):
    
    utm_x, utm_y = 0, 0

    selected = pd.DataFrame()
    selected = reference.iloc[reference.index.get_loc(timing, method='nearest')]

    x = float(selected.loc['lat'])
    y = float(selected.loc['lon'])
    
    if latlon == True:
        utm_x, utm_y = gmt2utm(y, x, +53)
    else:
        utm_x, utm_y = x, y

    return utm_x, utm_y


def printsps(sps):
    sys.stdout.write("{0:1s}{1:16s}{2:8d}{3:1d}{4:2d}{5:4d}".format(sps.record_identification,sps.line_name,sps.point_number,sps.point_index,sps.point_code,sps.static_correction))
    sys.stdout.write("{0:4.1f}{1:4d}{2:2d}{3:4.1f}".format(sps.point_depth,sps.seismic_datum,sps.uphole_time,sps.water_depth))
    sys.stdout.write("{0:9.1f}{1:10.1f}{2:6.1f}{3:3d}{4:6s}\n".format(sps.map_grid_easting,sps.map_grid_northing,sps.surface_elvation,sps.day_of_year,sps.time_hhmmss))

    return 0

def create_sps_from_descrete(s1, gpsfile):
    token=[]

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
            tr = segy.traces[j]
            hdr = segy.traces[j].header
            if hdr.trace_number_within_the_original_field_record == 1:
                strf = " ".join([str(hdr.year_data_recorded),str(hdr.day_of_year),str(hdr.hour_of_day),str(hdr.minute_of_hour),str(hdr.second_of_minute)])
                timing = datetime.strptime(strf,'%y %j %H %M %S')
                hms = datetime.strftime(timing,'%H%M%S')
                utm_x, utm_y = findxy_from_time(gpsdata, timing, latlon=True)

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
        for k in range(len(sps)):
            printsps(sps[k])

    return 0

def makesufgrp(basename):
    s1 = []
    for i in range(len(basename)):
        tape = WRKHOME + PATH_RAW + basename[i] + EXT_SGY
        sufile = WRKHOME + PATH_WRK + basename[i] + EXT_SU
        hfile = WRKHOME + PATH_HDR + PFX_HDR + basename[i] + EXT_TXT
        bfile = WRKHOME + PATH_HDR + PFX_BIN + basename[i] + EXT_BIN
        tmp_strm = Sufgrp(basename[i], tape, sufile, hfile, bfile)
        s1.append(tmp_strm)
#       print(s1[i].tape)
    return s1