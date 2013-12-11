#-*- coding: utf-8 -*-

u'''
https://wiki.python.org/moin/UdpCommunication
http://docs.python.org/2/library/socketserver.html
'''

import socket
import sys

SOCKET_PORT = 15225
RFCOMM_PORT = 3

def show_help_server(msg=None):
	if msg:
		print msg
	print '%s' % sys.argv[0]
    
def show_help_client(msg=None):
	if msg:
		print msg
	print '%s <ip>' % sys.argv[0]
    
def validate_client_argv():
    if len(sys.argv) != 2:
        show_help_client()
        return False
        
    ip = sys.argv[1]
    if not is_valid_ipv4_address(ip):
        show_help_client('Not valid IP')
        return False
    return True
    
def validate_server_argv():
    if len(sys.argv) != 1:
        show_help_server()
        return False
    return True
        

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def select_bluetooth_device(nearby_devices):
    for i, (bdaddr, name) in enumerate(nearby_devices):
        print "%d : %s <%s>" % (i, name, bdaddr)

    selected_index = raw_input('select device : ')
    try:
        selected_index = int(selected_index)
        selected_index = 0 if selected_index < 0 else selected_index
        selected_index = len(nearby_devices) if selected_index >= len(nearby_devices) else len(nearby_devices)-1
    except ValueError:
        selected_index = 0

    target_address, target_name = nearby_devices[selected_index]
    return target_address, target_name