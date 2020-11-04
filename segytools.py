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

basename = []

#basename.append('OB2001')
basename.append('OB2002')
#basename.append('OB2003')
#basename.append('OB2004')
#basename.append('OB2005_1-5440')
#basename.append('OB2005_5601-7381')
#basename.append('OB2006_1-2100')
#basename.append('OB2006_2201-5859')

#tape = []
#sufile = []
#header = []
#binary = []

class Sufgrp:
# class for su file group
    def __init__(self, tape, sufile, hfile, bfile):
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

def read_segy():
    #commands = []
    for i in range(len(basename)):
        command = ["segyread", "tape=" + s1[i].tape, "bfile=" + s1[i].bfile, "hfile=" + s1[i].hfile, "> " + s1[i].sufile]
        args = " ".join(command)

        print(args)
        os.system(args)

        #commands.append(command)
        #res = subprocess.run(commands[i])
    return 0

def sps2geom(spsfile):

    return 0 

def testsu():
    for i in range(len(basename)):

        command = ["sugethw", "key=tracl,fldr,year,day,minute,sec", "< " + s1[i].sufile]
        args = " ".join(command)        
        print(args)
#        os.system(args)

    return 0

def findxy_from_time(reference, timing, latlon):
#    print(reference)
    utm_x = 0
    utm_y = 0

    selected = pd.DataFrame()
    selected = reference.iloc[reference.index.get_loc(timing, method='nearest')]
#    print(selected)

    x = float(selected.loc['lat'])
    y = float(selected.loc['lon'])
    
    if latlon == True:
        utm_x, utm_y = gmt2utm(y, x, +53)
    else:
        utm_x, utm_y = x, y

    return utm_x, utm_y

def create_sps_from_descrete(gpsfile):
    token=[]

    gpsdata = pd.DataFrame()
    gpsdata = pd.read_csv(gpsfile,sep=",",names=['date_time','lat','lon'],\
                                       parse_dates=True, header=None)

    gpsdata['date_time'] = pd.to_datetime(gpsdata['date_time'])
    gpsdata.set_index(gpsdata['date_time'],drop=True, inplace=True)
    gpsdata = gpsdata.drop_duplicates(['date_time'])
    gpsdata = gpsdata.sort_index()

    for i in range(len(basename)):
#        segy = _read_segy_core(s1.tape[i],unpack_trace_headers=True)
#        print(segy.__str__(extended=True))
        sps = []
        segy = _read_segy_segy(s1[i].tape)
        for j in range(len(segy.traces)):

#        for j in range(100):
            tr = segy.traces[j]
            hdr = segy.traces[j].header
            if hdr.trace_number_within_the_original_field_record == 1:
                strf = " ".join([str(hdr.year_data_recorded),str(hdr.day_of_year),str(hdr.hour_of_day),str(hdr.minute_of_hour),str(hdr.second_of_minute)])
                timing = datetime.strptime(strf,'%y %j %H %M %S')
#                print(timing,hdr.original_field_record_number)
                hms = datetime.strftime(timing,'%H%M%S')
                utm_x, utm_y = findxy_from_time(gpsdata, timing, latlon=True)

                tmp_sps = spsfile(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                tmp_sps.record_identification = "S"
                tmp_sps.line_name = 0
                tmp_sps.point_number = hdr.original_field_record_number
                tmp_sps.point_index = 1
                tmp_sps.map_grid_easting = utm_x
                tmp_sps.map_grid_northing = utm_y
                tmp_sps.day_of_year = hdr.day_of_year
                tmp_sps.time_hhmmss = hms
                sps.append(tmp_sps)
        for k in range(len(sps)):
            print(sps[k].record_identification,sps[k].line_name,sps[k].point_number,sps[k].map_grid_easting,sps[k].map_grid_northing,sps[k].day_of_year,sps[k].time_hhmmss)

#        token.append(timing)
#        print(segy.traces[50].header)
    return 0

s1 = []
for i in range(len(basename)):
   tape = WRKHOME + PATH_RAW + basename[i] + EXT_SGY
   sufile = WRKHOME + PATH_WRK + basename[i] + EXT_SU
   hfile = WRKHOME + PATH_HDR + PFX_HDR + basename[i] + EXT_TXT
   bfile = WRKHOME + PATH_HDR + PFX_BIN + basename[i] + EXT_BIN
   tmp_strm = Sufgrp(tape,sufile,hfile,bfile)
   s1.append(tmp_strm)
   print(s1[i].tape)

#read_segy()
#testsu()
create_sps_from_descrete(WRKHOME+PATH_ASC+'202006_gpsdata'+EXT_TXT)