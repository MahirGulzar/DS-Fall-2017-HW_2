
import logging
import sys
from argparse import ArgumentParser
import os

from argparse import ArgumentParser
from sys import stdin, exit
from xmlrpclib import ServerProxy
from time import asctime, localtime
import sys
from os.path import sep, abspath
from sys import argv, path

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOG = logging.getLogger()


proxy=None
a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
path.append(a_path)
# print(a_path)
data_dir = '/data/'
download_dir ='/download/'
def main(args):
    # In this way ONLY one HANDLE is done, and that is fine, don't handle upload and download with same request.

    # Initialize server-proxy using RPC client
    # (connect to RPC service query the list of procedures exposed)

    global proxy
    # RPC Server's socket address
    server = (args.host, int(args.port))
    try:
        proxy = ServerProxy("http://%s:%d" % server)
    except KeyboardInterrupt:
        LOG.warn('Ctrl+C issued, terminating')
        exit(0)
    except Exception as e:
        LOG.error('Communication error %s ' % str(e))
        exit(1)

    LOG.info('Connected to File XMLRPC server!')
    methods = filter(lambda x: 'system.' not in x, proxy.system.listMethods())
    LOG.debug('Remote methods are: [%s] ' % (', '.join(methods)))


    check, data = proxy.Welcome_and_getList("Mahir",23212)
    print(check,data)
    grid = proxy.create_room("Mahir","custom_room")
    print(grid)





if __name__== "__main__":
    parser = ArgumentParser(description="Client for uploading/listing files.")
    parser.add_argument('-a', '--host', help="Address of the host. Default localhost.", default='127.0.0.1')
    parser.add_argument('-p', '--port', help="Listen on port.", default=19191, type=int)
    parser.add_argument('-u', '--upload', help="File to be uploaded.",nargs=1)
    # parser.add_argument('-l', '--list', help="List all the files in the server.", action='store_true')
    parser.add_argument('-d', '--download', help="Download specified file.",nargs=1)
    parser.add_argument('-r', '--remove', help="Remove specified file.",nargs=1)
    parser.add_argument('-m', '--move', help="Move specified file.",nargs=2)
    args = parser.parse_args()
    main(args)