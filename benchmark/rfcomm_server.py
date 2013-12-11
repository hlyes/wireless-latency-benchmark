#-*- coding: utf-8 -*-

u'''
https://code.google.com/p/pybluez/source/browse/tags/pybluez_0_18/examples/simple/rfcomm-server.py
'''

from bluetooth import *
import common

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

advertise_service(server_sock, "SampleServer",
                  service_id = common.UUID,
                  service_classes = [ common.UUID, SERIAL_PORT_CLASS ],
                  profiles = [ SERIAL_PORT_PROFILE ], 
                  #protocols = [ OBEX_UUID ] 
                  )
                   
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: 
            break
        client_sock.send(data)
        print "received [%s]" % data.strip()
except IOError:
    pass

print "disconnected"

client_sock.close()
server_sock.close()
print "all done"