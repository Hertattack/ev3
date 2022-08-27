SERVICE_UUID = "00001623 -1212-EFDE-1623-785FEABCD123"
CHARACTERISTIC_UUID = "00001624 -1212-EFDE-1623-785FEABCD123"


class ValueMapping:
    __NONE__ = '__None__'
    __MAPPING_PROPERTY__ = '__Mapping__'

    def __init__(self, value):
        if not hasattr(self, ValueMapping.__MAPPING_PROPERTY__):
            setattr(self, ValueMapping.__MAPPING_PROPERTY__, self.get_mapping())

        lookupValue = ValueMapping.__NONE__ if value is None else value

        if self.__Mapping__.__contains__(lookupValue):
            self.value = value
            self.name = self.__Mapping__[lookupValue]
        else:
            raise ProtocolError(f"Value {str(value)} is not supported in mapping.")

    def get_mapping(self):
        mapping = {}
        for item in dir(self):
            if item != ValueMapping.__MAPPING_PROPERTY__ and item.isupper():
                value = getattr(self, item)
                if value is None:
                    value = ValueMapping.__NONE__
                if mapping.__contains__(value):
                    raise Exception(f"Value mapping contains duplicate entry: {str(value)}")
                mapping[value] = item
        return mapping

    def __eq__(self, other):
        if type(self) == type(other):
            return self.value == other.value
        elif type(other) == bytes:
            return self.value == other

        return False


class VersionNumberEncoding:
    @classmethod
    def parse_bytes(cls, revision: bytes):
        if len(revision) > 5:
            raise ProtocolError("Version number cannot be more than 4 bytes.")

        major_and_minor = int.from_bytes(revision[0:1], byteorder="big", signed=False)
        major = (major_and_minor & int("11110000", 2)) % 15
        minor = major_and_minor & int("00001111", 2)
        patch = int(revision[1:2].hex())
        build = int(revision[2:].hex())

        return cls(major, minor, patch, build)

    def __init__(self, major: int, minor: int, patch: int, build: int):
        if 0 <= major <= 7 and 0 <= minor <= 9 and 0 <= patch <= 99 and 0 <= build <= 9999:
            self.major = major
            self.minor = minor
            self.patch = patch
            self.build = build
        else:
            raise ProtocolError(f"Unsupported version number. 0 <= {major} <= 7, 0 <= {minor} 9, 0 <= {patch} 99, 0 <= {build} <= 9999")

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
            raise ProtocolError(f"Unsupported version number. 0 <= {major} <= 99, 0 <= {minor} 99")

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
        self.length = int.from_bytes(byte_input[0], byteorder="big", signed=False)
        self.dataTypeName = byte_input[1]
        self.manufacturerId = int.from_bytes(bytes(byte_input[2:4]), byteorder="big", signed=False)
        self.buttonState = int.from_bytes(byte_input[4], byteorder="big", signed=False) == 1
        self.systemType = SystemTypeDeviceNumber(byte_input[5])
        self.capabilities = byte_input[6]
        self.last_network = byte_input[7]
        self.status = byte_input[8]
        self.option = byte_input[9]


class ProtocolError(Exception):
    def __init__(self, message, input_bytes=None):
        self.message = message
        self.input_bytes = input_bytes
