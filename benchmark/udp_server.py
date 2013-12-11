#!/usr/bin/env python
#-*- coding: utf-8 -*-

import common
import SocketServer
import sys
    
class UDPEchoHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        socket.sendto(data, self.client_address)
        print "{} wrote:".format(self.client_address[0]), data

def main():
    if not common.validate_server_argv():
        return -1
        
    HOST = "0.0.0.0"
    server = SocketServer.UDPServer((HOST, common.SOCKET_PORT), UDPEchoHandler)
    server.serve_forever()
    
if __name__ == '__main__':
    main()