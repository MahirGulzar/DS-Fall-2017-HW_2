import os
import threading
import logging
import pychat_util


'''
Importing sockets for server announcement over the network..
'''
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname


from argparse import ArgumentParser
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from SocketServer import ThreadingMixIn

from time import time
import sys
from os.path import sep, abspath
from sys import argv, path

# Please use LOGGING
FORMAT = '%(asctime)-15s %(levelname)s %(threadName)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()




#--------------------------------------------------------------------------------------------------------

'''
The RPC Server handles the main server side protocol of the game
whenever a client communicates with server, the server creates an object
of Hall and mark all the methods of Hall as RPC.. client can use these methods 
for further communication..
'''

#=============================================================================================


'''
Server Announcement on Local Network
'''
MAGIC = "fna349fn" #to make sure we don't confuse or get confused by other programs

def Server_Announcement(args):
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # for broadcast
    my_ip = args.laddr

    while 1:
        data = MAGIC + my_ip+" "+str(args.port)
        s.sendto(data, ('<broadcast>', args.port))
        #LOG.info("Announcing Server over the network...")
        sleep(1)



#=============================================================================================

'''
Multi-threading RPC Server to handle concurrent Client requests
'''

class MyXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

'''
Restric RPC to a particular path
'''
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)



class Server:
    def __init__(self, args):
        LOG.info("Server Started.")
        self.gameserver = pychat_util.Hall()
        self.server_sock = (args.laddr, args.port)
        # Create XML_server
        self.server = MyXMLRPCServer(self.server_sock,requestHandler=RequestHandler,allow_none=True)
        self.start_main()

    def start_main(self):

        self.server.register_introspection_functions()
        self.server.register_instance(self.gameserver)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print 'Ctrl+C issued, terminating ...'
        finally:
            self.server.shutdown()  # Stop the serve-forever loop
            self.server.server_close()  # Close the sockets
        LOG.info('Terminating ...')
        # Initilize RPC service on specific port
        # Register server-side functions into RPC middleware


'''
To Run RPC Server in Seperate Thread
'''
def Run_RPC(args):
    s = Server(args)

#=============================================================================================


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-l', '--laddr', help="Listen address. Default localhost.",  default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Listen on port.", default=12346, type=int)
    args = parser.parse_args()

    # Threads for server announcement over the network and
    # RPC Server Serve forever
    announce = threading.Thread(target=Server_Announcement, args=(args,))
    RPC_Feature = threading.Thread(target=Run_RPC,args=(args,))
    announce.start()
    RPC_Feature.start()
    announce.join()
    RPC_Feature.join()





