# import socket module
from socket import *

# In order to terminate the program
import sys
from threading import *
import threading
import time
import os

class ClientThread(Thread):
    def __init__(self, connectionSocket):
        Thread.__init__(self)
        #self.connectionSocket = socket
        #print("New server socket thread created" + str(threading.get_native_id()))
    
    def run(self):
            message = connectionSocket.recv(1024).decode() ### YOUR CODE HERE ###


            msg = message.split()[1]
            #print(msg)

            destaddr = msg.split("/")[1]
            filename = msg.split("/")[2]

            #print(filename)
            
            try:
                f = open(filename, "r")
                timestamp = f.readline()
                #print(timestamp)
                if (float(timestamp) < time.time() - 120):
                    os.remove(filename)
                    raise IOError
                else:
                    #connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                    output = f.read()
                    for i in range(0, len(output)):
                        connectionSocket.send(output[i].encode())
       
                    print("proxy-cache,client," + str(threading.get_native_id()) + "," + time.ctime())

            
            except IOError:

                #print("destaddr = " + destaddr)
                #print("filename = " + filename)

                sock = socket(AF_INET, SOCK_STREAM)
                
                addr = destaddr.split(":")[0]
                port = destaddr.split(":")[1]
                #print(addr)
                #print(port)

                msgToSend = "GET /" + filename
                #print(msgToSend)

                sock.connect((addr, int(port)))

                
                sock.send(msgToSend.encode())
                print("proxy-forward,server," + str(threading.get_native_id()) + "," + time.ctime())

                ret = sock.recv(4096)
                returnData = ""
                while ret:
                    returnData = returnData + ret.decode()
                    ret = sock.recv(4096)

                #print(returnData)
                tmp = open(filename, "w")
                tmp.write(str(time.time())+ "\n")
                tmp.write(returnData)
                tmp.close()
    

                connectionSocket.send(returnData.encode())
                print("proxy-forward,client," + str(threading.get_native_id()) + "," + time.ctime())

        

                

                # Send one HTTP header line into socket

                #connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) ### YOUR CODE HERE ###

                # Send the content of the requested file into socket

                # Close client socket
            connectionSocket.close()
        


# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
### YOUR CODE HERE ###
serverPort = 800
serverSocket.bind(("", serverPort))
threads = []


serverSocket.listen(4)


while True:
    # Establish the connection
    #print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    newthread = ClientThread(connectionSocket)
    newthread.start()
    threads.append(newthread)
    

        # Close client socket
     ### YOUR CODE HERE ###

# Close server socket

serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
