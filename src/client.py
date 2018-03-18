
import sys
import argparse
import logging
import base64
import socket

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client chat interface for '
                                                 'the L_orang robot.')
    parser.add_argument('address', type=str, nargs='?',
                        default='Silent-Assassin.lan',
                        help='address of the L_orang server.')
    parser.add_argument('port', type=int, nargs='?', default='1337',
                        help='port number of the L_orang server.')

    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((args.address, args.port))
        logging.debug('Connection successful')
        while True:
            # Print interface
            sys.stdout.write('me> ')
            sys.stdout.flush()

            # Read user input
            user_text = sys.stdin.readline()
            user_text = user_text[:(len(user_text) - 1)]

            # Construct socket message
            base64_text = base64.b64encode(user_text.encode('utf-8'))
            msg = base64_text + b':EOS:'

            # Send socket message
            logging.debug('Sending message')
            total_bytes = 0
            while total_bytes < len(msg):
                bytes_sent = client_socket.send(msg[total_bytes:])
                logging.debug('Sent ' + str(bytes_sent) + '/' + str(len(msg))
                              + ' bytes')
                if bytes_sent == 0:
                    raise RuntimeError('Connection error')
                total_bytes += bytes_sent

            logging.debug('Message successfully sent')
    finally:
        logging.debug('Closing socket')
        client_socket.close()
