#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import subprocess
import logging
import SocketServer

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

def log(host, data):

    logger = logging.getLogger('mpk')
    logger.setLevel(logging.INFO)

    # create file handler
    fh = logging.FileHandler(config.LOGFILE)
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(message)s %(host)s %(data)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    # shout out the message
    d = { 'host' : host, 'data' : data }
    logger.info('Port knocked by: ', extra=d)

    # remove handlers until needed again
    logger.removeHandler(ch)
    logger.removeHandler(fh)


class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        log(self.client_address[0], data)
        if data == "ssh":
            lockup(self.client_address[0], 22)
            
if __name__ == "__main__":
    HOST, PORT = config.HOST, config.MAGIC_PORT
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()

