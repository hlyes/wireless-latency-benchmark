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
    msg_generator = common.EchoGenerator(maxcount=common.LOOP_COUNT)
    history_container = common.TimeHistoryContainer()
    while True:
        data = msg_generator()
        if len(data) == 0: 
            break

        try:
            watch = common.StopWatch()
            sock.sendto(data, (HOST, common.SOCKET_PORT))
            received = sock.recv(1024)
            latency = watch.stop()
            history_container.append(latency)
            #print "received [%s]" % received
        except socket.timeout:
            #print 'timeout'
            history_container.append(999)
    
    latency_list = history_container.get_stats_list(reverse=False)
    for x in latency_list:
        print x
        
if __name__ == '__main__':
    main()