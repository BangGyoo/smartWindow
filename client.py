import sys
import socket
def decoding(a):
    a=a
    b=a.decode()
    print(b)

temp = ""
for i in sys.argv[1:] :
	temp += i + " "
msg=bytearray(temp,'utf-8') 
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err :
    print("error : %s"%(err))
 
port=4321
 
s.connect(('',port))
#decoding(s.recv(1024))
s.send(msg)

s.close()


