import socket

# UDP (forward to)
HOST = ''
PORT = 50001
ADDRESS = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TCP Client (listen source #2)
host = "127.0.0.1"
port = 50000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
     response = client.recv(4096)
     s.sendto(response, (ADDRESS, PORT))
     sentences = str(response).replace('\\','').replace('b\'','').replace('\'','').strip().split('r')
     for i in range(len(sentences)-1):
         print(sentences[i])
         tokens = sentences[i].split(',')    
         if tokens[0] == '$GPRMC':
            print(tokens[3],tokens[4],tokens[5],tokens[6])

