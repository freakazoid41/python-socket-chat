import socket
import sys
from _thread import *
import time
import json

host=''
port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.bind((host,port))
except socket.error as e:
    print(str(e))
s.listen(5)
clients = []

print("waiting for connection .....")
def threaded_client(conn,port):
    User = json.loads(conn.recv(2048))
    User=dict({'id':User["id"],'name':User["name"],'conn':conn})
    clients.append(User)
    conn.send(str.encode("welcome "+User["name"]+", type your info.. \n"))
    print(str(User))
    while True:
        data=conn.recv(2048)
        target = str(str(data).split(":")[0]).replace("b'pickle","")
        reply=str(port+" / "+User["name"]+': '+data.decode('utf-8')).replace("pickle"+str(target)+":"," ")
        print(reply)
        print(target)
        if not data:
            break
        else:
            try:
                target=next(item for item in clients if item["id"] == int(target))
                target['conn'].send(str.encode(reply))
            except:
                conn.send(str.encode("'{clientid}:' please fill client id and put ' : ' then write your message.."))
                print ("Please write client id...")

    conn.close()




while True:
    conn,addr=s.accept()
    print('Connected to : '+addr[0]+" : "+str(addr[1]))
    start_new_thread(threaded_client,(conn,str(addr[1])))
