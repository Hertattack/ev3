SERVICE_UUID = "00001623 -1212-EFDE-1623-785FEABCD123"
CHARACTERISTIC_UUID = "00001624 -1212-EFDE-1623-785FEABCD123"


class MessageTypes:
    # Hub Related
    HUB_PROPERTY = b'\x01'
    HUB_ACTION = b'\x02'
    HUB_ALERT = b'\x03'
    HUB_ATTACHED_IO = b'\x04'
    GENERIC_ERROR_MSG = b'\x05'
    HW_NW_COMMAND = b'\x08'
    FW_UPDATE_BOOT = b'\x10'
    FW_UPDATE_LOCK_MEM = b'\x11'
    FW_UPDATE_LOCK_STATUS_REQ = b'\x12'
    FW_LOCK_STATUS = b'\x13'

    # Port related
    PORT_INFO_REQ = b'\x21'
    PORT_MODE_INFO_REQ = b'\x22'
    PORT_INPUT_FORMAT_SETUP_SINGLE = b'\x41'
    PORT_INPUT_FORMAT_SETUP_COMBINED = b'\x42'
    PORT_INFO = b'\x43'
    PORT_MODE_INFO = b'\x44'
    PORT_VALUE_SINGLE = b'\x45'
    PORT_VALUE_COMBINED = b'\x46'
    PORT_INPUT_FORMAT_SINGLE = b'\x47'
    PORT_INPUT_FORMAT_COMBINED = b'\x48'
    VIRTUAL_PORT_SETUP = b'\x61'
    PORT_OUTPUT_COMMAND = b'\x81'
    PORT_OUTPUT_COMMAND_FEEDBACK = b'\x82'


class CommonMessageHeader:
    """
    Common Header for all messages

    Size = 3 bytes.
    """
    HUB_ID = b'\x00'

    def __init__(self, messageLength, messageType):
        self.messageLength = messageLength
        self.messageType = messageType

    def getValue(self):
        actualLength = self.messageLength + 3
        if actualLength <= 127:
            return actualLength.to_bytes(1, byteorder="big", signed=False) + \
                   CommonMessageHeader.HUB_ID + \
                   self.messageType
        else:
            actualLength = actualLength + 1
            remainder = actualLength % 127
            multiplier = (actualLength - remainder) // 127
            return (remainder + 127).to_bytes(1, byteorder='big', signed=False) + multiplier.to_bytes(1,
                                                                                                      byteorder='big',
                                                                                                      signed=False) + CommonMessageHeader.HUB_ID + self.messageType


class VersionNumberEncoding:
    def __init__(self, major, minor, patch, build):
        if 0 <= major <= 7 and 0 <= minor <= 9 and 0 <= patch <= 99 and 0 <= build <= 9999:
            self.major = major
            self.minor = minor
            self.patch = patch
            self.build = build
        else:
            raise f"Unsupported version number. 0 <= {major} <= 7, 0 <= {minor} 9, 0 <= {patch} 99, 0 <= {build} <= 9999"

    def getValue(self):
        return int(f"{self.major}{self.minor}", 16).to_bytes(1, byteorder="big") + \
               int(f"{self.patch}", 16).to_bytes(1, byteorder="big") + \
               int(f"{self.build}", 16).to_bytes(2, byteorder="big")


class LWPVersionNumberEncoding:
    def __init__(self, major, minor):
        if 0 <= major <= 99 and 0 <= minor <= 99:
            self.major = major
            self.minor = minor
        else:
            raise f"Unsupported version number. 0 <= {major} <= 99, 0 <= {minor} 99"

    def getValue(self):
        return int(f"{self.major}{self.minor}", 16).to_bytes(2, byteorder="big")