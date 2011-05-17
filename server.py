#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import subprocess
import logging
import SocketServer

logger = logging.getLogger('mpk')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def lockup(host, port):
    """Allow port access from defined host """
    rule = ("/sbin/iptables",
    "-I", "INPUT",
    "-p", "tcp",
    "-m", "state",
    "--state", "NEW,ESTABLISHED",
    "--dport", str(port),
    "--source", host,
    "-j", "ACCEPT",
    )
    subprocess.Popen(rule)

class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        logger.info("Port %s knocked by %s" % (data, self.client_address[0]))
        if data == "ssh":
            lockup(self.client_address[0], 22)
            
if __name__ == "__main__":
    HOST, PORT = config.HOST, config.MAGIC_PORT
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()

