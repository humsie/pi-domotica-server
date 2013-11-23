#!/usr/bin/python

import socket               # Import socket module
import ConfigParser

#from plugins import *
import plugins
print dir(plugins)

class DomoServer:

    def import_class(self, cl):
        (modulename, classname) = cl.rsplit('.', 2)
        m = __import__(modulename, globals(), locals(), [classname])
        return getattr(m, classname)

    def __init__(self):

        self.config = ConfigParser.SafeConfigParser(defaults=None, allow_no_value=True)
        self.config.read('DomoServer.cfg')

        self.debug = self.config.get('server','debug')
        self.host = self.config.get('server','host')
        print self.host;
        self.port = self.config.getint('server','port')


        self.messages = {}
        for i in dir(plugins):
            if (i[0:2]!="__"):
                temp = self.import_class("plugins.%s" % (i))
                self.messages[temp.getIdentifier()] = self.import_class("plugins.%s" % (i))(self)


    def startServer(self):
        print "Starting server..., waiting at port: %s" % (self.port) 
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)                 # Now wait for client connection.
        while True:
            connection, addr = self.socket.accept()     # Establish connection with client.

            msg = connection.recv(1024)
            msg = msg.split("\n")
            i = 0
            while i < len(msg):
                if (msg[i].strip() != ""):
                    parts = msg[i].split(":", 1)
                    self.messages[parts[0]].receive(parts[1])
                i = i + 1
            
            connection.close()


if __name__ == '__main__':
    domoServer = DomoServer()
    domoServer.startServer()