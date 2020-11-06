# Convert NMEA 0183 powered by micropyGPS
# Convert .l16 log files exported from SeaPath by H.Otsuka
#                                              19 Oct 2020

import sys
import micropyGPS
import pandas as pd
#from geotools import *
import pgeotools as pg

#gps = micropyGPS.MicropyGPS(9, 'dd') # JST
gps = micropyGPS.MicropyGPS(0, 'dd') # UTC

l16 = pd.DataFrame(columns=['year','month','day','hour','minute','seconds','lat','lon'], index=[0,1,2,3,4,5])
sec_cache = 0

def nmearead(sentence):

    for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
        gps.update(x)

    h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
    year, month, day = gps.date[2], gps.date[1], gps.date[0]
    hour, minute, seconds = h, gps.timestamp[1], gps.timestamp[2]
    lon_now, lat_now = gps.longitude[0], gps.latitude[0]

    return year, month, day, hour, minute, seconds, lat_now, lon_now


def l16read(sentence, l16):
    year, month, day, hour, minute, seconds, lat_now, lon_now = 0,0,0,0,0,0,0,0
    londms = [0]*3
    latdms = [0]*3
    sig_lat = 1
    sig_lon = 1

    token = sentence.split(',')
    for l in range(len(token)):
        if  len(token[l]) == 0:
            token[l] = "00000000000000"

    if token[0] in {'$INZDA'}:
        l16.loc[0,'year'] = int(token[4][2:])
        l16.loc[0,'month'] = int(token[3])
        l16.loc[0,'day'] = int(token[2])
        timestamp = token[1]
        l16.loc[0,'hour'] = int(timestamp[0:2])
        l16.loc[0,'minute'] = int(timestamp[2:4])
        l16.loc[0,'seconds'] = float(timestamp[4:])

    if token[0] in {'$INGGA'}:
        timestamp = token[1]
        l16.loc[0,'hour'] = int(timestamp[0:2])
        l16.loc[0,'minute'] = int(timestamp[2:4])
        l16.loc[0,'seconds'] = float(timestamp[4:])

        if token[3] == "S": sig_lat = -1
        if token[5] == "W": sig_lon = -1

        latdms[0] = int(token[2][0:2])
        latdms[1] = float(token[2][2:])
        londms[0] = int(token[4][0:3])
        londms[1] = float(token[4][3:])
        latdms[2] = londms[2] = 0

        l16.loc[0,'lat'] = pg.dms2dec(latdms * sig_lat)
        l16.loc[0,'lon'] = pg.dms2dec(londms * sig_lon)
        
        l16 = l16.shift(1).fillna(0)



    l16.fillna(0,inplace=True)
    year = l16.loc[1,'year']
    month = l16.loc[1,'month']
    day = l16.loc[1,'day']
    
    hour = l16.loc[1,'hour']
    minute = l16.loc[1,'minute']
    seconds = l16.loc[1,'seconds']
    lat_now = l16.loc[1,'lat']
    lon_now = l16.loc[1,'lon']

    return year, month, day, hour, minute, seconds, lat_now, lon_now, l16


#MAIN
year, month, day, hour, minute, seconds, lat_now, lon_now = 0,0,0,0,0,0,0,0
for line in sys.stdin:
    sentence = line #line.decode('utf-8')
    if sentence[0] != '$': # 先頭が'$'でなければ捨てる
        continue
    if sentence[1] == 'I':
        year, month, day, hour, minute, seconds, lat_now, lon_now, l16 = l16read(sentence, l16)        
    if sentence[1] == 'G':
        year, month, day, hour, minute, seconds, lat_now, lon_now = nmearead(sentence)        

#    print(l16)
    if sec_cache != seconds:
       print('20%02d/%02d/%02d %2d:%02d:%04.1f, ' % (year, month, day, hour, minute, seconds),end="")
       print('%2.8f, %2.8f' % (lat_now, lon_now))

    sec_cache = seconds
