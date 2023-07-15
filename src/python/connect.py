#!/usr/bin/env python3
import asyncio
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

async def main(ble_address: str):
    print(ble_address)
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError("A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)
            service.uuid


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else "90:84:2B:66:5B:2B"))
gi