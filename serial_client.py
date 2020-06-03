import socket
import serial

# UDP (forward to)
HOST = ''
PORT = 50001
ADDRESS = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Serial (source #1)
#ser = serial.Serial('/dev/ttyUSB0', 4800)
ser = serial.Serial('/dev/tty.usbserial', 4800)

while True:
     response = ser.readline()
#     response = serline.encode
     s.sendto(response, (ADDRESS, PORT))
#     print ("----------------------------------------")
#     print(response)
#     print ("----------------------------------------")
     sentence = response.decode().strip()
     print(sentence)   

#     sentences = str(response).replace('\\','').replace('b\'','').replace('\'','').strip().split('r')
#     for i in range(len(sentences)-1):
#         print(sentences[i])
#         tokens = sentences[i].split(',')    
#         if tokens[0] == '$GPRMC':
#            print(tokens[3],tokens[4],tokens[5],tokens[6])

