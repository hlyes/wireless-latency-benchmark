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
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data)

def main():
    if not common.validate_server_argv():
        return -1
        
    HOST = "0.0.0.0"
    server = SocketServer.TCPServer((HOST, common.PORT), TCPEchoHandler)
    server.serve_forever()
    
if __name__ == '__main__':
    main()