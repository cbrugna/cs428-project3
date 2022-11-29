# import socket module
from socket import *

# In order to terminate the program
import sys
from threading import *
import threading

class ClientThread(Thread):
    def __init__(self, connectionSocket):
        Thread.__init__(self)
        #self.connectionSocket = socket
        print("New server socket thread created" + str(threading.get_native_id()))
    
    def run(self):
        try:
            message = connectionSocket.recv(1024) ### YOUR CODE HERE ###
        
            print('Message is: ', message)

            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read() ### YOUR CODE HERE ###

            # Send one HTTP header line into socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) ### YOUR CODE HERE ###

            # Send the content of the requested file into socket
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

            # Close client socket
            connectionSocket.close()
        except IOError:
            # Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode()) 
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()) ### YOUR CODE HERE ###
            connectionSocket.close()


# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
### YOUR CODE HERE ###
serverPort = 960
serverSocket.bind(("", serverPort))
threads = []


serverSocket.listen(4)


while True:
    # Establish the connection
    print('Ready to serve...')
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