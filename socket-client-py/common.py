#-*- coding: utf-8 -*-

u'''
https://wiki.python.org/moin/UdpCommunication
http://docs.python.org/2/library/socketserver.html
'''

import socket
import sys

PORT = 15225

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