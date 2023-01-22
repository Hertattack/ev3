import asyncio

from src.util.scanning import Scanner

from .base import BaseIntegrationTest


class Scanning(BaseIntegrationTest):
    __name__ = "Scanning test"

    def __implementation__(self, args):
        scanner = Scanner()
        asyncio.run(scanner.scan(self.__handle_device_found__))

    def __handle_device_found__(self, device, advertising_data):
        print(device)
        print(advertising_data)
