import socket
def decoding(a):
    a=a
    b=a.decode()
    print(b)
 
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error as err :
    print("error : %s"%(err))
 
port=1234
 
s.connect(('localhost',port))
decoding(s.recv(1024))

s.close()


