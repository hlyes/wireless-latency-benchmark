#-*- coding: utf-8 -*-

import bluetooth
import common

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_sock.bind(("", common.RFCOMM_PORT))
server_sock.listen(1)

client_sock, address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
print "received [%s]" % data

client_sock.close()
server_sock.close()