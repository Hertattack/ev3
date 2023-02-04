import asyncio
from bleak import BleakScanner


class Scanner:

    def __init__(self):
        self.__is_started__ = False
        self.__discovery_function__ = None
        self.__stop_event__ = asyncio.Event()
        self.__scanner__ = BleakScanner(detection_callback=self.__detect__, scanning_mode='active')

    def __detect__(self, device, advertising_data):
        if self.__discovery_function__ is not None:
            self.__discovery_function__(device, advertising_data)

    async def scan(self, discovery_function):
        if self.__is_started__:
            raise "Already running"

        self.__discovery_function__ = discovery_function

        self.__is_started__ = True
        await self.__scanner__.start()

        await self.__stop_event__.wait()
        self.__is_started__ = False

    def stop_scan(self):
        if not self.__is_started__:
            self.__discovery_function__ = None
            return

        self.__scanner__.stop()
        self.__discovery_function__ = None

        self.__stop_event__.set()
