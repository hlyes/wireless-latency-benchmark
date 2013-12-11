#!/usr/bin/env python
#-*- coding: utf-8 -*-

import common
import SocketServer
import sys
    
class TCPEchoHandler(SocketServer.StreamRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        for x in range(common.LOOP_COUNT):
            self.data = self.rfile.readline().strip()
            self.wfile.write(self.data)
            print "{} wrote:".format(self.client_address[0]), self.data

def main():
    if not common.validate_server_argv():
        return -1
        
    HOST = "0.0.0.0"
    server = SocketServer.TCPServer((HOST, common.SOCKET_PORT), TCPEchoHandler)
    server.serve_forever()
    
if __name__ == '__main__':
    main()