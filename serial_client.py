import socket
import serial
import pyproj
import micropyGPS
import threading
import time

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



while True:
#     response = ser.readline()
#     skt.sendto(response, (ADDRESS, PORT))

#     sentence = response.decode().strip()
#     print(sentence)   

#     sentences = str(response).replace('\\','').replace('b\'','').replace('\'','').strip().split('r')
#     for i in range(len(sentence)-1):
#         print(sentences[i])
#     tokens = sentence.split(',')    
#     if tokens[0] == '$GPRMC':
#        strings=tokens[3] + "," + tokens[4] + "," + tokens[5] + "," + tokens[6]
#        print('\033[31m' + strings + '\033[0m')
    if gps.clean_sentences > 20: # ちゃんとしたデーターがある程度たまったら出力する
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        print('%2d:%02d:%04.1f' % (h, gps.timestamp[1], gps.timestamp[2]))
        print('緯度経度: %2.8f, %2.8f' % (gps.latitude[0], gps.longitude[0]))
        print('海抜: %f' % gps.altitude)
        print(gps.satellites_used)
        print('衛星番号: (仰角, 方位角, SN比)')
        for k, v in gps.satellite_data.items():
            print('%d: %s' % (k, v))
        print('')
    time.sleep(1.0)
