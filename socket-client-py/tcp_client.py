#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import common
import sys
import socket

def main():    
    if not common.validate_client_argv():
        return -1    
    
    msg_generator = common.EchoGenerator(maxcount=common.LOOP_COUNT)
    history_container = common.TimeHistoryContainer()

    HOST = sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, common.SOCKET_PORT))
    except IOError:
        print >> sys.stderr, 'cannot connect'
        return -1

    while True:
        data = msg_generator()
        if len(data) == 0: 
            break

        watch = common.StopWatch()
        sock.sendall(data)
        received = sock.recv(1024)
        latency = watch.stop()
        history_container.append(latency)
    sock.close()

    latency_list = history_container.get_stats_list(reverse=False)
    for x in latency_list:
        print x
        
if __name__ == '__main__':
    main()