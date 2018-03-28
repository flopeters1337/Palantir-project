
import sys
import argparse
import logging
import socket
from Crypto.Cipher import AES
from definitions import aes_passphrase, aes_iv
from palantir_socket import PalantirSocket
logging.basicConfig(level=logging.INFO)

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 1337
BUFFER_SIZE = 4096


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client chat interface for '
                                                 'the Palantir assistant.')
    parser.add_argument('address', type=str, nargs='?',
                        default=DEFAULT_HOST,
                        help='address of the Palantir server.')
    parser.add_argument('port', type=int, nargs='?', default=DEFAULT_PORT,
                        help='port number of the Palantir server.')

    args = parser.parse_args()

    client_socket = PalantirSocket(BUFFER_SIZE,
                                   AES.new(aes_passphrase,
                                           AES.MODE_CBC,
                                           aes_iv),
                                   family=socket.AF_INET,
                                   socket_type=socket.SOCK_STREAM)

    try:
        client_socket.connect(args.address, args.port)
        logging.debug('Connection successful')
        sys.stdout.write('Now connected to Palantir. Type \':exit\' to '
                         'exit the program.\n')
        while True:
            # Print interface
            sys.stdout.write('?> ')
            sys.stdout.flush()

            # Read user input
            user_text = sys.stdin.readline()
            user_text = user_text[:(len(user_text) - 1)]
            if user_text == ':exit':
                logging.debug('Now exiting')
                break

            # Send socket message
            logging.debug('Sending message')
            client_socket.send(user_text)

            logging.debug('Message successfully sent')

            # Wait for answer from server
            string = client_socket.rcv()

            sys.stdout.write('(Palantir)> ' + string + '\n')

            logging.debug('Closing socket')
            client_socket.close()

            client_socket = PalantirSocket(BUFFER_SIZE,
                                           AES.new(aes_passphrase,
                                                   AES.MODE_CBC,
                                                   aes_iv),
                                           family=socket.AF_INET,
                                           socket_type=socket.SOCK_STREAM)
            client_socket.connect(args.address, args.port)
            logging.debug('Connection successful')
    finally:
        logging.debug('Closing socket')
        client_socket.close()
