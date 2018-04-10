
import pytest
from threading import Thread
from time import sleep
from src.server import PalantirServer


class TestServer:
    @staticmethod
    def test_basic_initialization():
        server = PalantirServer()
        assert isinstance(server, PalantirServer)

    @staticmethod
    def test_run_server():
        server = PalantirServer()
        test_thread = Thread(target=server.run)
        test_thread.setDaemon(True)
        test_thread.start()
        sleep(1)
        assert test_thread.is_alive()
