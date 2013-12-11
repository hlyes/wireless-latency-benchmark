#-*- coding: utf-8 -*-

u'''
https://wiki.python.org/moin/UdpCommunication
http://docs.python.org/2/library/socketserver.html
'''

import time
import socket
import sys

SOCKET_PORT = 15225

UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

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
    except ValueError:
        selected_index = 0

    target_address, target_name = nearby_devices[selected_index]
    return target_address, target_name

class StopWatch(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = time.clock()
        self.stop_time = None

    def stop(self):
        u'''
        result type is millisecond, NOT SECOND!!
        '''
        self.stop_time = time.clock()
        return (self.stop_time - self.start_time) * 1000

class TimeHistoryContainer(object):
    def __init__(self):
        self.time_list = []

    def append(self, dt):
        self.time_list.append(dt)

    def get_stats_list(self, remove_first_last=False, reverse=False):
        u'''
        sort time list
        if remove_first_last enabled, remove smallest value and largest value
        if reverse : True=>desc, False=>asc
        '''
        assert len(self.time_list) >= 2

        time_list = sorted(self.time_list, reverse=reverse)
        if remove_first_last:
            return time_list[1:-1]
        else:
            return time_list

class EchoGenerator(object):
    def __init__(self, fmt=None, maxcount=10):
        if not fmt:
            fmt = '%032d'
        self.fmt = fmt
        self.count = 1
        self.maxcount = maxcount

    def __call__(self):
        if self.maxcount < self.count:
            return ''
        msg = self.fmt % self.count
        self.count += 1
        return msg