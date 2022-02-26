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

    def __init__(self, message_length: int, message_type: bytes):
        self.messageLength = message_length
        self.messageType = message_type

    @property
    def value(self):
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

    @property
    def value(self):
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

    @property
    def value(self):
        return int(f"{self.major}{self.minor}", 16).to_bytes(2, byteorder="big")


class SystemTypeDeviceNumber:
    LEGO_WEDO_HUB = int('00000000',2)
    LEGO_DUPLO_TRAIN = int('00100000',2)
    LEGO_BOOST_HUB = int('01000000',2)
    LEGO_2_PORT_HUB = int('01000001',2)
    LEGO_2_PORT_HANDSET = int('01000010',2)

    MAPPING = {
        LEGO_WEDO_HUB: "LEGO_WEDO_HUB",
        LEGO_DUPLO_TRAIN: "LEGO_DUPLO_TRAIN",
        LEGO_BOOST_HUB: "LEGO_BOOST_HUB",
        LEGO_2_PORT_HUB: "LEGO_2_PORT_HUB",
        LEGO_2_PORT_HANDSET: "LEGO_2_PORT_HANDSET"
    }

    def __init__(self, system_type: bytes):
        if type(system_type) != bytes:
            raise "Expected bytes as input."

        self.value = system_type
        self.int_value = int.from_bytes(system_type, byteorder="big", signed=False)

        if SystemTypeDeviceNumber.MAPPING.__contains__(self.int_value):
            self.name = SystemTypeDeviceNumber.MAPPING[self.int_value]
        else:
            raise "Unsupported system type."


class AdvertisingMessage:

    def __init__(self, byte_input: bytes):
        bytearray_input: bytearray = bytearray(byte_input)
        self.length = int.from_bytes(bytearray_input[0], byteorder="big", signed=False)
        self.dataTypeName = bytearray_input[1]
        self.manufacturerId = int.from_bytes(bytes(bytearray_input[2:3]), byteorder="big", signed=False)
        self.buttonState = int.from_bytes(bytearray_input[4], byteorder="big", signed=False) == 1
        self.systemType = SystemTypeDeviceNumber(bytearray_input[5])