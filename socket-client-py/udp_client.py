#!/usr/bin/env python
#-*- coding: utf-8 -*-

import common
import sys
import socket

def main():    
    if not common.validate_client_argv():
        return -1    
    
    '''
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto('test msg', (ip, PORT))
	'''
    HOST = sys.argv[1]

    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1);

    # As you can see, there is no connect() call; UDP has no connections.
    # Instead, data is directly sent to the recipient via sendto().
    #data = 'hello world'
    data = 'hel'
    sock.sendto(data + '\n', (HOST, common.PORT))

    received = sock.recv(1024)
    print "Sent:     {}".format(data)
    print "Received: {}".format(received)
        
if __name__ == '__main__':
    main()