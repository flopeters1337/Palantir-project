
import sys
import argparse
import logging
import base64
import socket
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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((args.address, args.port))
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

            # Wait for answer from server
            msg = b''
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if chunk is b'':
                    raise RuntimeError('Socket connection broken')
                msg += chunk

                # If we have received an End Of String token
                if ':EOS:' in chunk.decode('utf-8'):
                    logging.debug("Received message : \"" + str(msg) + "\"")
                    base64_string = msg[:(len(msg) - 5)]
                    string = base64.b64decode(base64_string).decode('utf-8')
                    break

            sys.stdout.write('(Palantir)> ' + string + '\n')

            logging.debug('Closing socket')
            client_socket.close()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((args.address, args.port))
            logging.debug('Connection successful')
    finally:
        logging.debug('Closing socket')
        client_socket.close()
