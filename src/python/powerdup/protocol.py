SERVICE_UUID="00001623 -1212-EFDE-1623-785FEABCD123"
CHARACTERISTIC_UUID="00001624 -1212-EFDE-1623-785FEABCD123"

class LegoWireless:

    def __init__(self):
        pass

"""
Common Header for all messages

Size = 3 bytes.
"""
class CommonMessageHeader:
    HUB_ID=b'\x00'

    def __init__(self, messageLength):
        self.messageLength = messageLength

    def getValue(self):
        if(self.messageLength <= 127):
            return self.messageLength.to_bytes(1,byteorder="big", signed=False) + self.HUB_ID
        else:
            remainder = self.messageLength % 127
            multiplier = (self.messageLength - remainder) / 127 + 1
            return (remainder+128).to_bytes(1,byteorder='big',signed=False) + multiplier.to_bytes(1,byteorder='big',signed=False) + self.HUB_ID
