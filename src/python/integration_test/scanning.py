import asyncio
from time import sleep

from src.platform import GetScanner
from .base import BaseIntegrationTest


class Scanning(BaseIntegrationTest):
    __name__ = "Scanning test"

    def __implementation__(self, args):
        scanner = GetScanner()
        asyncio.run(scanner.scan(self.__handle_device_found__))

        sleep(10)
        scanner.stop_scan()

    def __handle_device_found__(self, device, advertising_data):
        print(device)
        print(advertising_data)
