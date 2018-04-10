
import logging
import argparse
from server import PalantirServer
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]:%(levelname)s: %(message)s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Palantir server command.')
    parser.add_argument('--local', dest='hostname', action='store_const',
                        const='localhost', default='',
                        help='run the server on localhost.')
    parser.add_argument('port', type=int, nargs='?', default=1337,
                        help='port number for the server.')
    args = parser.parse_args()

    server = PalantirServer(args.hostname, args.port)
    server.run()
