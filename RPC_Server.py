import os
import threading
import logging
import pychat_util

from argparse import ArgumentParser
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from time import time
import sys
from os.path import sep, abspath
from sys import argv, path

# Please use LOGGING
FORMAT = '%(asctime)-15s %(levelname)s %(threadName)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()




# Restrict to a particular path.
class FileServerRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class Server:
    def __init__(self, args):
        LOG.info("Server Started.")
        self.gameserver = pychat_util.Hall()
        self.server_sock = (args.laddr, args.port)
        # Create XML_server
        self.server = SimpleXMLRPCServer(self.server_sock)
        self.start_main()

    def start_main(self):
        #start the RPC server


        self.server.register_introspection_functions()

        self.server.register_instance(self.gameserver)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print 'Ctrl+C issued, terminating ...'
        finally:
            self.server.shutdown()  # Stop the serve-forever loop
            self.server.server_close()  # Close the sockets
        print 'Terminating ...'
        # Initilize RPC service on specific port

        # Register server-side functions into RPC middleware


# NB! READ ARGPARSER DESCRIPTION IN CLIENT, if confused by argparsers
if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-l', '--laddr', help="Listen address. Default localhost.",  default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Listen on port.", default=19191, type=int)
    args = parser.parse_args()
    s = Server(args)