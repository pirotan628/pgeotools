import socket
import serial
import pyproj
import micropyGPS
import threading
import time
#from bottle import Bottle, run

#-------------------------------------
#app = Bottle()
#
#@app.route('/hello')
#def hello():
#    return "Hello World!"
#
#run(app, host='localhost', port=8080)
#-------------------------------------
#
grs80 = pyproj.Geod(ellps='GRS80')  # GRS80楕円体
gps = micropyGPS.MicropyGPS(9, 'dd') # JST

# UDP (forward to)
HOST = ''
PORT = 50001
ADDRESS = "127.0.0.1"
skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Serial (source)
dev = '/dev/tty.usbserial'  # MacOS
#dev = '/dev/ttyUSB0'        # Linux
brate = 4800                # borate for BU-353S4 Module


def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    ser = serial.Serial(dev, brate, timeout=10)    
    ser.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        response = ser.readline()
        skt.sendto(response, (ADDRESS, PORT))
        sentence = response.decode('utf-8')
        print(sentence.strip())   

        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)

gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
gpsthread.daemon = True
gpsthread.start() # スレッドを起動

lon_ref, lat_ref = 135.292489, 34.717932  # 深江
declination = -7.5

while True:
    if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24

        hour, minute, seconds = h, gps.timestamp[1], gps.timestamp[2]
        lon_now, lat_now = gps.longitude[0], gps.latitude[0]

        azimuth, bkw_azimuth, distance = grs80.inv(lon_now, lat_now, lon_ref, lat_ref)
        azm_mag, bkw_azm_mag = azimuth - declination, bkw_azimuth + declination
        nauticalmile = distance / 1852

        print('\033[31m',end="")        
        print('%2d:%02d:%04.1f' % (hour, minute, seconds))
        print('%2.8f, %2.8f' % (lat_now, lon_now))
        print(azimuth, bkw_azimuth, distance, nauticalmile)
        print(azm_mag, bkw_azm_mag, end="")
        print('\033[0m')

    time.sleep(1.0)
