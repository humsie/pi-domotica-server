#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import sys
import ConfigParser


config = ConfigParser.SafeConfigParser(defaults=None, allow_no_value=True)
config.read('client.cfg')

s = socket.socket()         # Create a socket object
host = config.get('server', 'host') # Get local machine name
port = config.getint('server', 'port')                # Reserve a port for your service.


data = sys.stdin.readlines()
print "Counted", len(data), "lines."

s.connect((host, port))
s.send("\n".join(data));
#for line in data:
#    s.send(line);

s.close                     # Close the socket when done


#s.send('rgb:0:255:255:0:255:255:0:255:255:0');
#s.send('rgb:0:0:0:0:0:0:0:0:0:0');
