
import logging
import base64
import socket
from threading import Thread
logging.basicConfig(level=logging.INFO)

PORT_NUMBER = 1337
BUFFER_SIZE = 4096


def handle_client(client_socket):
    msg = b''

    try:
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if chunk is b'':
                raise RuntimeError('Socket connection broken')
            msg += chunk

            # If we have received an End Of String token
            if ':EOS:' in chunk.decode('utf-8'):
                base64_string = msg[:(len(msg) - 5)]
                string = base64.b64decode(base64_string).decode('utf-8')

                # Handle message
                logging.info('Received message "' + string + '"')

                # Reset message buffer
                msg = b''
    finally:
        client_socket.close()


if __name__ == '__main__':
    # Initialize server socket
    logging.info('Initializing server')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    server_socket.bind((hostname, PORT_NUMBER))

    # Listen for connections
    logging.info('Listening on port ' + str(PORT_NUMBER) + ' with hostname ' +
                 hostname)
    server_socket.listen(5)

    # Main loop
    try:
        while True:
            try:
                logging.info('Waiting for requests')
                (client_socket, address) = server_socket.accept()
                logging.info('Received client connection')
                ct = Thread(target=handle_client, args=[client_socket])
                ct.run()
            except Exception as e:
                logging.error(type(e).__name__ + ': "' + str(e)
                              + '" Now recovering')
    finally:
        server_socket.close()
