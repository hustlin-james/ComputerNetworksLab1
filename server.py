
#https://stackoverflow.com/questions/35372867/simple-multithreaded-web-server-in-python
from socket import *
import threading
import time
import sys
import pdb
import os

class serverThread(threading.Thread):
    def __init__(self, serverPort):
        threading.Thread.__init__(self)
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.connectionThreads = []
    def run(self):
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(1)
        while True:
            #Establish the connection
            print('Ready to serve...')
            connectionSocket,addr = self.serverSocket.accept()
            message = connectionSocket.recv(1024) #Get message
            print("Message recieved, opening new thread")
            self.connectionThreads.append(connectionThread(connectionSocket, message))
            self.connectionThreads[-1].daemon = 1
            self.connectionThreads[-1].start()
    def close(self):
        for t in self.connectionThreads:
            try:
                t.connSocket.shutdown(SHUT_RDWR)
                t.connSocket.close()
            except socket.error:
                pass
        self.serverSocket.shutdown(SHUT_RDWR)
        self.serverSocket.close()

class connectionThread (threading.Thread):
    def __init__(self, connSocket, message):
        threading.Thread.__init__(self)
        self.connSocket = connSocket
        self.message = message
    def run(self):
        try:
            filename = self.message.split()[1] #Getting requested HTML page
            f = open(filename[1:]) #Opening data stream from HTML
            file_size = os.path.getsize(filename[1:])
            outputdata = f.read() #Reading HTML page
            f.close() #Closing data stream from HTML
            self.connSocket.send("HTTP/1.0 200 OK") #Send one HTTP header line into socket
            content_length = "Content-Length: "+str(file_size)+"\n"
            self.connSocket.send(content_length)
            self.connSocket.send(outputdata)
            # for i in range(0, len(outputdata)): #Send the content of the requested file to the client
            #     self.connSocket.send(outputdata[i])
        except IOError: #Triggered if user requests bad link
            self.connSocket.send("404 Not Found") #Send response message for file not found
        finally:
            self.connSocket.shutdown(SHUT_RDWR)
            self.connSocket.close()

def main():
    port = 8080
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])

    print("listening on %d"%port)
    server = serverThread(int(port))
    server.daemon = 1
    server.start()
    end = raw_input("Press enter to stop server...")
    server.close()
    print("Program complete")


if __name__ == "__main__":
    main()
