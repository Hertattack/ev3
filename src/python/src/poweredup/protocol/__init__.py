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
        self.length = int.from_bytes(byte_input[0], byteorder="big", signed=False)
        self.dataTypeName = byte_input[1]
        self.manufacturerId = int.from_bytes(bytes(byte_input[2:4]), byteorder="big", signed=False)
        self.buttonState = int.from_bytes(byte_input[4], byteorder="big", signed=False) == 1
        self.systemType = SystemTypeDeviceNumber(byte_input[5])
        self.capabilities = byte_input[6]
        self.last_network = byte_input[7]
        self.status = byte_input[8]
        self.option = byte_input[9]

