#!/usr/bin/env python
#-*- coding: utf-8 -*-

import common
import sys
import socket

def main():    
    if not common.validate_client_argv():
        return -1    
    
    HOST = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    data = 'hel'
    
    try:
        # Connect to server and send data
        sock.connect((HOST, common.BLUETOOTH_PORT))
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()

    print "Sent:     {}".format(data)
    print "Received: {}".format(received)

        
if __name__ == '__main__':
    main()