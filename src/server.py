
import argparse
import logging
import base64
import socket
import json
from multiprocessing.pool import ThreadPool
from palantir_socket import PalantirSocket
logging.basicConfig(level=logging.INFO)

DEFAULT_PORT = 1337
BUFFER_SIZE = 4096
POOL_SIZE = 50


def handle_client(client_socket):
    client_socket = PalantirSocket(BUFFER_SIZE, socket_obj=client_socket)
    client_host, client_port = client_socket.getpeername()
    client_name = client_host + ':' + str(client_port)
    logging.info('[' + client_name + ']: Now handling')

    try:
        string = client_socket.rcv()
        logging.info('[' + client_name + ']: "' + string + '"')

        # Send the reply
        client_socket.send(string)
        logging.info('[' + client_name + ']: Reply successfully sent')
    finally:
        logging.info('[' + client_name + ']: Closing connection')
        client_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Palantir server command.')
    parser.add_argument('--local', dest='hostname', action='store_const',
                        const='localhost', default='',
                        help='run the server on localhost.')
    parser.add_argument('port', type=int, nargs='?', default=DEFAULT_PORT,
                        help='port number for the server.')
    args = parser.parse_args()

    # Initialize thread pool
    logging.info('Creating thread pools of size ' + str(POOL_SIZE))
    pool = ThreadPool(POOL_SIZE)

    # Initialize server socket
    logging.info('Initializing server socket')
    server_socket = PalantirSocket(BUFFER_SIZE,
                                   family=socket.AF_INET,
                                   socket_type=socket.SOCK_STREAM)
    server_socket.bind(args.hostname, args.port)

    # Listen for connections
    logging.info('Listening on port ' + str(args.port))
    server_socket.listen(5)

    # Main loop
    try:
        while True:
            try:
                logging.info('Waiting for requests')
                (client_socket, address) = server_socket.accept()
                logging.info('Received client connection')
                pool.map_async(handle_client, [client_socket])
            except Exception as e:
                logging.error(type(e).__name__ + ': "' + str(e)
                              + '" Now recovering')
    finally:
        server_socket.close()
