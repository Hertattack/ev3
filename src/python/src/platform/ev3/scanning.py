import asyncio
from bluepy.btle import Scanner as BtleScanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self, discovery_function):
        DefaultDelegate.__init__(self)
        self._handler = discovery_function

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

        self._handler(dev, None)

class Scanner:

    def __init__(self):
        self._scanner_impl = None

    async def scan(self, discovery_function):
        if self._scanner_impl is not None:
            raise "Scanner already initialized"

        self._scanner_impl = BtleScanner().withDelegate(ScanDelegate(discovery_function))

        self._scanner_impl.scan(10)

        await asyncio.sleep(10, result='hello')

    def stop_scan(self):
        pass