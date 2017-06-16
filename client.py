#!/usr/bin/env python
 
import socket
 

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
BUFFER_SIZE = 1024
MESSAGE = "GET /file.html HTTP/1.1"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
data = s.recv(BUFFER_SIZE)
content_length = int(data.split()[1])
data = s.recv(content_length)
s.close()

if __name__ == "__main__":
    #client_code_name <server_IPaddress/name> [<port_number>] [<requested_file_name>]
    main()


