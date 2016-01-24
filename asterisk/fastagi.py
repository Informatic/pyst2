#!/usr/bin/env python
# FastAGI service for Asterisk
# Requires modified pyst2 to support reading stdin/out/err
#
# Copyright 2011 VOICE1, LLC
# By: Ben Davis <ben@voice1-dot-me>

import SocketServer
import asterisk.agi
import logging

logger = logging.getLogger(__name__)
# import pkg_resources
# PYST_VERSION = pkg_resources.get_distribution("pyst2").version

__verison__ = 0.1

# TODO: Read options from config file.
HOST, PORT = "127.0.0.1", 4573


class FastAGI(SocketServer.StreamRequestHandler):
    # Close connections not finished in 5seconds.
    timeout = 5

    def handle(self):
        try:
            agi = asterisk.agi.AGI(stdin=self.rfile, stdout=self.wfile)
            agi.verbose("pyst2: FastAGI on: {}:{}".format(HOST, PORT))
        except TypeError:
            logger.exception('Unable to connect to agi://{}'.format(
                self.client_address[0]))
        except SocketServer.socket.timeout:
            logger.exception('Timeout receiving data from {}'.format(
                self.client_address))
        except SocketServer.socket.error:
            logger.exception('Could not open the socket. Is someting else '
                             'listening on this port?')
        except Exception:
            logger.exception('An unknown error')

if __name__ == "__main__":
    # server = SocketServer.TCPServer((HOST, PORT), FastAGI)
    server = SocketServer.ForkingTCPServer((HOST, PORT), FastAGI)

    # Keep server running until CTRL-C is pressed.
    server.serve_forever()
