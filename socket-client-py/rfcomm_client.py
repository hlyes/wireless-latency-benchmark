#-*- coding: utf-8 -*-

u'''
https://code.google.com/p/pybluez/source/browse/trunk/examples/simple/rfcomm-client.py
'''
from bluetooth import *
import sys
import common

addr = None

if len(sys.argv) < 2:
    print >> sys.stderr, "no device specified.  Searching all nearby bluetooth devices for"
    print >> sys.stderr, "the SampleServer service"
else:
    addr = sys.argv[1]
    print >> sys.stderr, "Searching for SampleServer on %s" % addr

# search for the SampleServer service
service_matches = find_service( uuid = common.UUID, address = addr )

if len(service_matches) == 0:
    print >> sys.stderr, "couldn't find the SampleServer service =("
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print >> sys.stderr, "connecting to \"%s\" on %s" % (name, host)

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))

#print "connected.  type stuff"
msg_generator = common.EchoGenerator(maxcount=common.LOOP_COUNT)
history_container = common.TimeHistoryContainer()
while True:
    data = msg_generator()
    if len(data) == 0: 
        break

    watch = common.StopWatch()
    sock.send(data)
    data = sock.recv(1024)
    latency = watch.stop()
    history_container.append(latency)

sock.close()

latency_list = history_container.get_stats_list(reverse=False)
for x in latency_list:
    print x
