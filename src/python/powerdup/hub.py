from bleak import BleakScanner
from bleak import BleakClient

class Hub:
    def __init__(self):
        pass
    async def connect(self):
        self.device = await BleakScanner.find_device_by_filter(hubFilter, timeout=120.0)
        if not self.device:
            raise ConnectionError("No hub found.")
        else:
            self.client = await BleakClient(self.device).connect()

def hubFilter(device, data):
    if('00001623-1212-efde-1623-785feabcd123' in data.service_uuids):
        print("Found Lego Hub")
        return True