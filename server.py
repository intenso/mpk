#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import shlex, subprocess
import SocketServer

def lockup(host, port):
    """Allow port access from defined host """
    rule = "/sbin/iptables -A INPUT -p tcp -m state --state NEW --dport %s --source %s -j ACCEPT" % (port, host)
    args = shlex.split(rule)
    subprocess.Popen(args)
    
class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "Knock-knock by: %s" % self.client_address[0]
        print "Code word: %s" % data
        if data == "ssh":
            lockup(self.client_address[0], 22)
            
if __name__ == "__main__":
    HOST, PORT = config.HOST, config.MAGIC_PORT
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()