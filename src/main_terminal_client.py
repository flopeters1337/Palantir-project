
import logging
import argparse
from client import TerminalClient
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]:%(levelname)s: %(message)s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client chat interface for '
                                                 'the Palantir assistant.')
    parser.add_argument('address', type=str, nargs='?',
                        default='localhost',
                        help='address of the Palantir server.')
    parser.add_argument('port', type=int, nargs='?', default=1337,
                        help='port number of the Palantir server.')
    args = parser.parse_args()

    client = TerminalClient(server_address=args.address, server_port=args.port)
    client.run()
