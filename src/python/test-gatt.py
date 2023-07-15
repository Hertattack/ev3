#!/usr/bin/env python3

from ev3dev.auto import *
from gattlib import GATTRequester
from time import sleep

address = "90:84:2B:66:5B:2B"
HANDLE = 0x3d
SPIN_LEFT = "\x01\x01\x01\x64"
SPIN_RIGHT = "\x01\x01\x01\x9C"
SPIN_STOP = "\x01\x01\x01\x00"
DELAY = 0.3  # this is empiric - the WeDo seems to need this delay
# between each command

ts = TouchSensor();

req = GATTRequester(address, True, "hci0")
sleep(DELAY)

command = SPIN_LEFT
while True:
    if ts.value():
        if (req.is_connected() == True):
            print("Already connected")
            sleep(DELAY)
        else:
            print("Connecting...")
            req.connect(True)
            print("OK")
            sleep(DELAY)

        req.write_by_handle(HANDLE, command)

        if (command == SPIN_LEFT):
            command = SPIN_RIGHT
        else:
            command = SPIN_LEFT
        sleep(DELAY)

    if (req.is_connected() == True):
        print("Still connected")
    else:
        print("Reconnecting...")
        req.connect(True)
        print("OK")
        sleep(DELAY)