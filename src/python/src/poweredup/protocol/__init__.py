SERVICE_UUID = "00001623 -1212-EFDE-1623-785FEABCD123"
CHARACTERISTIC_UUID = "00001624 -1212-EFDE-1623-785FEABCD123"


class ValueMapping:

    def __init__(self, value):
        if not hasattr(self, "MAPPING"):
            setattr(self, "MAPPING", self.get_mapping())

        if self.MAPPING.__contains__(value):
            self.value = value
            self.name = self.MAPPING[value]
        else:
            raise f"Value {str(value)} is not supported in mapping."

    def get_mapping(self):
        mapping = {}
        for item in dir(self):
            if item != "MAPPING" and item.isupper():
                value = getattr(self, item)
                mapping[value] = item
        return mapping


class MessageType(ValueMapping):
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
    @classmethod
    def decode(cls, revision: bytes):
        if len(revision) > 4:
            raise "Version number cannot be more than 4 bytes."

        major_and_minor = revision[0]
        major = (major_and_minor & int("11110000", 2)) % 15
        minor = major_and_minor & int("00001111", 2)
        patch = revision[1]
        build = int.from_bytes(revision, byteorder="big", signed=False) & int("11111111", 2)

        return cls(major, minor, patch, build)

    def __init__(self, major: int, minor: int, patch: int, build: int):
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


class SystemTypeDeviceNumber(ValueMapping):
    LEGO_WEDO_HUB = b'\x00'
    LEGO_DUPLO_TRAIN = b'\x20'
    LEGO_BOOST_HUB = b'\x40'
    LEGO_2_PORT_HUB = b'\x41'
    LEGO_2_PORT_HANDSET = b'\x42'


class AdvertisingMessage:

    def __init__(self, byte_input: bytes):
        bytearray_input: bytearray = bytearray(byte_input)
        self.length = int.from_bytes(bytearray_input[0], byteorder="big", signed=False)
        self.dataTypeName = bytearray_input[1]
        self.manufacturerId = int.from_bytes(bytes(bytearray_input[2:3]), byteorder="big", signed=False)
        self.buttonState = int.from_bytes(bytearray_input[4], byteorder="big", signed=False) == 1
        self.systemType = SystemTypeDeviceNumber(bytearray_input[5])
        self.capabilities = bytearray_input[6]
        self.last_network = bytearray_input[7]
        self.status = bytearray_input[8]
        self.option = bytearray_input[9]
