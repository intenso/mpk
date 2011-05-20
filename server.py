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
    try:
        subprocess.check_call(rule)
        logger.info("Port %s opened for %s" % (port, host))
    except:
        logger.error("Iptables failed for port %s and host %s" % (port, host))

class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        host = self.client_address[0]
        logger.info("Port %s knocked by %s" % (data, host))
        if data == "ssh":
            lockup(host, 22)
        else:
            logger.warning("%s provided bad message: %s" % (host, data))
            
if __name__ == "__main__":
    HOST, PORT = config.HOST, config.MAGIC_PORT
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()

