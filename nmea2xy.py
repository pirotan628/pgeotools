import sys
import pyproj
import micropyGPS

grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体
#gps = micropyGPS.MicropyGPS(9, 'dd') # JST
gps = micropyGPS.MicropyGPS(0, 'dd') # UTC
#346c8ea027f72

def nmearead(sentence):

    for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
        gps.update(x)

    h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
    year, month, day = gps.date[2], gps.date[1], gps.date[0]
    hour, minute, seconds = h, gps.timestamp[1], gps.timestamp[2]
    lon_now, lat_now = gps.longitude[0], gps.latitude[0]

    return year, month, day, hour, minute, seconds, lat_now, lon_now
    
def l16read(sentence):

    for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
        gps.update(x)
    #ToDo
    # make all features
    

    h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
    year, month, day = gps.date[2], gps.date[1], gps.date[0]
    hour, minute, seconds = h, gps.timestamp[1], gps.timestamp[2]
    lon_now, lat_now = gps.longitude[0], gps.latitude[0]

    return year, month, day, hour, minute, seconds, lat_now, lon_now

#MAIN
for line in sys.stdin:
    sentence = line #line.decode('utf-8')
    if sentence[0] != '$': # 先頭が'$'でなければ捨てる
        continue
    if sentence[1] == 'I':
        print('l16 ',end="")
        year, month, day, hour, minute, seconds, lat_now, lon_now = l16read(sentence)        
    if sentence[2] == 'G':
        year, month, day, hour, minute, seconds, lat_now, lon_now = nmearead(sentence)

    print('20%02d/%02d/%02d %2d:%02d:%04.1f, ' % (year, month, day, hour, minute, seconds),end="")
    print('%2.8f, %2.8f' % (lat_now, lon_now))
