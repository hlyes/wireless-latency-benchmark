#-*- coding: utf-8 -*-

u'''
https://code.google.com/p/pybluez/source/browse/trunk/examples/simple/rfcomm-client.py
'''
from bluetooth import *
import sys
import common

addr = None

if len(sys.argv) < 2:
    print "no device specified.  Searching all nearby bluetooth devices for"
    print "the SampleServer service"
else:
    addr = sys.argv[1]
    print "Searching for SampleServer on %s" % addr

# search for the SampleServer service
service_matches = find_service( uuid = common.UUID, address = addr )

if len(service_matches) == 0:
    print "couldn't find the SampleServer service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

print "connected.  type stuff"
while True:
    data = raw_input()
    if len(data) == 0: 
    	break
    sock.send(data)
    data = sock.recv(1024)
    print "received [%s]" % data
sock.close()
