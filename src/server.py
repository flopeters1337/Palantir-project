
import logging
import base64
import socket
from threading import Thread
logging.basicConfig(level=logging.INFO)

PORT_NUMBER = 1337


def handle_client(client_socket):
    pass


if __name__ == '__main__':
    # Initialize server socket
    logging.info('Initializing server')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), PORT_NUMBER))

    # Listen for connections
    logging.info('Listening on port ' + str(PORT_NUMBER))
    server_socket.listen(5)

    # Main loop
    while True:
        try:
            logging.info('Waiting for requests')
            (client_socket, address) = server_socket.accept()
            logging.info('Received client connection')
            ct = Thread(target=handle_client, args=client_socket)
            ct.run()
        except Exception as e:
            logging.error('Caught ' + str(type(e)) + ': "' + str(e)
                          + '" Now recovering')
