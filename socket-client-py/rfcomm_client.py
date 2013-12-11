#-*- coding: utf-8 -*-

import bluetooth
import common

nearby_devices = bluetooth.discover_devices(lookup_names=True)
if len(nearby_devices) == 0:
	print 'no nearby bluetooth devices'
	raise SystemExit(-1)

target_address, target_name = common.select_bluetooth_device(nearby_devices)


sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, RFCOMM_PORT))

sock.send('hello!')
sock.close()
