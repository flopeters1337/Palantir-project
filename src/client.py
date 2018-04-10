
import sys
import argparse
import logging
import socket
from Crypto.Cipher import AES
from definitions import aes_passphrase, aes_iv
from palantir_socket import PalantirSocket


class TerminalClient:
    def __init__(self, buffer_size: int = 4096,
                 server_address: str = 'localhost', server_port: int = 1337):
        """

        """
        self.__buffer_size = buffer_size
        self.__server_address = server_address
        self.__server_port = server_port

    def run(self):
        """

        :return:
        """
        client_socket = PalantirSocket(self.__buffer_size,
                                       AES.new(aes_passphrase,
                                               AES.MODE_CBC,
                                               aes_iv),
                                       family=socket.AF_INET,
                                       socket_type=socket.SOCK_STREAM)

        try:
            sys.stdout.write('Type \':exit\' to '
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

                # Connect to Palantir server
                client_socket.connect(self.__server_address,
                                      self.__server_port)
                logging.debug('Connection successful')

                # Send socket message
                logging.debug('Sending message')
                client_socket.send(user_text)

                logging.debug('Message successfully sent')

                # Wait for answer from server
                string = client_socket.rcv()

                sys.stdout.write('(Palantir)> ' + string + '\n')

                logging.debug('Closing socket')
                client_socket.close()
        finally:
            logging.debug('Closing socket')
            client_socket.close()
