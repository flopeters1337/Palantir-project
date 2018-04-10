
from threading import Thread
from src.server import PalantirServer
from src.client import TerminalClient


class TestTerminalClient:
    @staticmethod
    def test_exit_client(monkeypatch):
        # Mock user input
        monkeypatch.setattr('sys.stdin.readline', lambda: ':exit\n')

        client = TerminalClient()
        client.run()

    @staticmethod
    def test_client_server(monkeypatch):
        # Mock user input
        class MockClass:
            counter = 0

            def mock_input(self):
                if self.counter == 1:
                    return ':exit\n'
                elif self.counter == 0:
                    self.counter += 1
                    return 'lorem ipsum dolor sit amet\n'

        mock_object = MockClass()
        monkeypatch.setattr('sys.stdin.readline', mock_object.mock_input)

        # Initialize server
        server = PalantirServer(port=1338)
        server_thread = Thread(target=server.run)
        server_thread.setDaemon(True)
        server_thread.start()

        # Launch client
        client = TerminalClient(server_address='', server_port=1338)
        client.run()
