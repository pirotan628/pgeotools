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

basename.append('OB2001')
#basename.append('OB2002')
#basename.append('OB2003')
#basename.append('OB2004')
#basename.append('OB2005_1-5440')
#basename.append('OB2005_5601-7381')
#basename.append('OB2006_1-2100')
#basename.append('OB2006_2201-5859')

tape = []
sufile = []
header = []
binary = []

def read_segy():
    #commands = []
    for i in range(len(basename)):
        command = ["segyread", "tape=" + tape[i], "bfile=" + binary[i], "hfile=" + header[i], "> " + sufile[i]]
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

        command = ["sugethw", "key=tracl,fldr,year,day,minute,sec", "< " + sufile[i]]
        args = " ".join(command)        
        print(args)
#        os.system(args)

    return 0

def create_sps_from_descrete(gpsfile):
    token=[]
    gpsdata = pd.DataFrame()
    gpsdata = pd.read_csv(gpsfile,sep=",",names=['date_time','lat','lon'],dtype=object, header=None)
    for i in range(len(basename)):
#        segy = _read_segy_core(tape[i],unpack_trace_headers=True)
#        print(segy.__str__(extended=True))

        segy = _read_segy_segy(tape[i])
        for j in range(len(segy.traces)):
#        for j in range(100):
            tr = segy.traces[j]
            hdr = segy.traces[j].header
            if hdr.trace_number_within_the_original_field_record == 1:
                strf = " ".join([str(hdr.year_data_recorded),str(hdr.day_of_year),str(hdr.hour_of_day),str(hdr.minute_of_hour),str(hdr.second_of_minute)])
                timing = datetime.strptime(strf,'%y %j %H %M %S')
                print(timing,hdr.original_field_record_number)
                hms = datetime.strftime(timing,'%H%M%S')
        
        token.append(timing)
        token.append("S")
        token.append(0)
        token.append(0)
        token.append(1)
        token.append(0)
        token.append(0)
        token.append(0)
        token.append(0)
        token.append(0)
        token.append(0)
        token.append("lon")
        token.append("lat")
        token.append(0)
        token.append(hdr.day_of_year)
        token.append(hms)

        print(token)
        print(segy.traces[50].header)
    return 0


for i in range(len(basename)):
   tape.append(WRKHOME + PATH_RAW + basename[i] + EXT_SGY)
   sufile.append(WRKHOME + PATH_WRK + basename[i] + EXT_SU)
   header.append(WRKHOME + PATH_HDR + PFX_HDR + basename[i] + EXT_TXT)
   binary.append(WRKHOME + PATH_HDR + PFX_BIN + basename[i] + EXT_BIN)

#read_segy()
#testsu()
create_sps_from_descrete(WRKHOME+PATH_ASC+'202006_gpsdata'+EXT_TXT)