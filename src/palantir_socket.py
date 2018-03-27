
import socket
import base64


class PalantirSocket:

    def __init__(self, buffer_size, family=None, socket_type=None,
                 socket_obj=None):
        """Default constructor

        :param buffer_size: Buffer size to use for socket messages.
        :param family:      Family of sockets to use (Same values as for
                            regular sockets). Default is None.
        :param socket_type: Type of sockets to use (Same values as for regular
                            sockets). Default is None.
        :param socket_obj:  A regular socket object.

        Note: At least either 'socket_obj' or both 'family' and 'socket_type'
        have to be specified to instantiate the socket.
        """
        self.__buffer_size = buffer_size
        if socket_obj is None:
            self.__socket = socket.socket(family, socket_type)
        else:
            self.__socket = socket_obj

    def bind(self, hostname, port):
        self.__socket.bind((hostname, port))

    def connect(self, address, port):
        self.__socket.connect((address, port))

    def listen(self, num_connections):
        self.__socket.listen(num_connections)

    def send(self, message):
        # Construct socket message
        base64_text = base64.b64encode(message.encode('utf-8'))
        msg = base64_text + b':EOS:'

        total_bytes = 0
        while total_bytes < len(msg):
            bytes_sent = self.__socket.send(msg[total_bytes:])
            if bytes_sent == 0:
                raise RuntimeError('Broken pipe')
            total_bytes += bytes_sent

    def rcv(self):
        msg = b''

        while True:
            chunk = self.__socket.recv(self.__buffer_size)
            if chunk is b'':
                raise RuntimeError('Broken pipe')
            msg += chunk

            # If we have received an End Of String token
            if ':EOS:' in chunk.decode('utf-8'):
                base64_string = msg[:(len(msg) - 5)]
                string = base64.b64decode(base64_string).decode('utf-8')
                break

        return string

    def accept(self):
        return self.__socket.accept()

    def close(self):
        self.__socket.close()

    def getpeername(self):
        return self.__socket.getpeername()
