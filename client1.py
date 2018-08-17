import socket
import threading

host = "192.168.1.123"
port = 5555
calistir = (host,port)

istemci = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
istemci.connect(calistir)
print("Connected...")
m ='{"id": 3, "name": "client1"}'
istemci.send(str.encode(m))

def YourLedRoutine():
    while True:
        data=istemci.recv(2048)
        if not data:
            print("input is empty")
        else:
            print(str(data.decode('utf-8')))



t1 = threading.Thread(target=YourLedRoutine)
#Background thread will finish with the main program
t1.setDaemon(True)
#Start YourLedRoutine() in a separate thread
t1.start()



while True:
    data=input()
    if not data:
        data="Boş Konu"
    istemci.send(str.encode(data))
