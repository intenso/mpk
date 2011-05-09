#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import socket
import sys

HOST, PORT = config.HOST, config.MAGIC_PORT

data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(data + "\n", (HOST, PORT))

print "Sent:     %s" % data
