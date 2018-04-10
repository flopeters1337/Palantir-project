
import logging
import socket
from multiprocessing.pool import ThreadPool
from Crypto.Cipher import AES
from definitions import aes_passphrase, aes_iv
from palantir_socket import PalantirSocket


class PalantirServer:
    """Class that inmplements a Palantir server used as the main unit of the
    Palantir system"""
    def __init__(self, hostname: str = 'localhost', port: int = 1337,
                 buffer_size: int = 4096, pool_size: int = 50):
        """Default constructor

        :param hostname:    Hostname for the server's socket
        :param port:        Port number for the server's socket
        :param buffer_size: Buffer size for messages used by the server's
                            socket
        :param pool_size:   Number of threads to instantiate in the thread pool
        """
        logging.info('Creating thread pool of size ' + str(pool_size))
        self.__pool = ThreadPool(pool_size)

        logging.info('Initializing server socket on ' + hostname + ':'
                     + str(port))
        self.__buffer_size = buffer_size
        self.__socket = PalantirSocket(buffer_size, None,
                                       family=socket.AF_INET,
                                       socket_type=socket.SOCK_STREAM)
        self.__socket.bind(hostname, port)

    def run(self):
        """Run the server so that it can accept client connections

        :return:    Make the server's socket listen to incoming connections
                    and handle them accordingly.
        """
        self.__socket.listen(5)
        logging.info('Now running')
        try:
            while True:
                try:
                    logging.info('Waiting for requests')
                    (client_socket, address) = self.__socket.accept()

                    logging.info('Received client connection')
                    self.__pool.map_async(PalantirServer.handle_client,
                                          [(client_socket,
                                            self.__buffer_size)])
                except Exception as e:
                    logging.error(type(e).__name__ + ': "' + str(e)
                                  + '" Now recovering')
        finally:
            self.__socket.close()

    @staticmethod
    def handle_client(args):
        client_socket, buffer_size = args
        client_socket = PalantirSocket(buffer_size,
                                       AES.new(aes_passphrase,
                                               AES.MODE_CBC,
                                               aes_iv),
                                       socket_obj=client_socket)
        client_host, client_port = client_socket.getpeername()
        client_name = client_host + ':' + str(client_port)
        logging.info('[' + client_name + ']: Now handling')

        try:
            string = client_socket.rcv()
            logging.info('[' + client_name + ']: "' + string + '"')

            # Send the reply
            client_socket.send(string)
            logging.info('[' + client_name + ']: Reply successfully sent')
        except Exception as e:
            logging.error('[' + client_name + ']:' + type(e).__name__ + ": "
                          + str(e))
        finally:
            logging.info('[' + client_name + ']: Closing connection')
            client_socket.close()

