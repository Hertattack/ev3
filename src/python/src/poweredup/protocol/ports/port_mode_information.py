import struct

from src.poweredup.protocol import ProtocolError, ValueMapping
from src.poweredup.protocol.messages import Message, MessageType, CommonMessageHeader
from src.poweredup.protocol.ports.port import PortID


class ModeInformationType(ValueMapping):
    NAME = b'\x00'
    RAW = b'\x01'
    PERCENTAGE = b'\x02'
    SI = b'\x03'
    SYMBOL = b'\x04'
    MAPPING = b'\x05'
    INTERNAL_USE = b'\x06'
    MOTOR_BIAS = b'\x07'
    CAPABILITY_BITS = b'\x08'
    VALUE_FORMAT = b'\x80'


class PortModeCombinationIndex(ValueMapping):
    INDEX_0 = b'\x01'
    INDEX_1 = b'\x02'
    INDEX_2 = b'\x03'
    INDEX_3 = b'\x04'
    INDEX_4 = b'\x05'
    INDEX_5 = b'\x06'
    INDEX_6 = b'\x07'
    INDEX_7 = b'\x08'


class PortModeInformationType(ValueMapping):
    NAME = b'\x00'
    RAW = b'\x01'
    PERCENTAGE = b'\x02'
    SI = b'\x03'
    SYMBOL = b'\x04'
    MAPPING = b'\x05'
    INTERNAL = b'\x06'
    MOTOR_BIAS_PCT = b'\x07'
    CAPABILITIES = b'\x08'
    VALUE_FORMAT = b'\x80'


class PortModeInformationRequestMessage(Message):
    MESSAGE_TYPE = MessageType.PORT_MODE_INFO_REQ

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 3:
            raise ProtocolError("Message too long")

        portId = PortID(message_bytes[0:1])
        modeInformation = ModeInformationType(message_bytes[2:])
        return PortModeInformationRequestMessage(portId, message_bytes[1:2], modeInformation)

    def __init__(self, port_id: PortID, mode: bytes, mode_information: ModeInformationType):
        self.port_id = port_id
        self.mode = mode
        self.mode_information = mode_information

    @property
    def value(self):
        header = CommonMessageHeader(3, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.mode + self.mode_information.value


class PortModeMapping:

    @classmethod
    def parse_bytes(cls, message_bytes):
        if len(message_bytes) > 1:
            raise ProtocolError("Expected a single byte for the port mode mapping")

        value = message_bytes[0]
        null_value_mapping = value & 128 == 128
        functional_mapping_2 = value & 64 == 64
        absolute_mapping = value & 16 == 16
        relative_mapping = value & 8 == 8
        discrete_mapping = value & 4 == 4

        return PortModeMapping(null_value_mapping, functional_mapping_2,
                               absolute_mapping, relative_mapping, discrete_mapping)

    def __init__(self, null_value, functional_mapping_2, absolute, relative, discrete):
        self.null_value = null_value
        self.functional_mapping_2 = functional_mapping_2
        self.absolute = absolute
        self.relative = relative
        self.discrete = discrete

    @property
    def value(self):
        value = (128 if self.null_value else 0) + \
                ( 64 if self.functional_mapping_2 else 0) + \
                ( 16 if self.absolute else 0) + \
                (  8 if self.relative else 0) + \
                (  4 if self.discrete else 0)

        return value.to_bytes(1, byteorder="big")


def build_index():
    PortModeInformationFormat.__implementations__ = {}
    for subclass in PortModeInformationFormat.__subclasses__():
        if hasattr(subclass, "MODE_INFORMATION_TYPE"):
            PortModeInformationFormat.__implementations__[subclass.MODE_INFORMATION_TYPE.value] = subclass
        else:
            for sub_subclass in subclass.__subclasses__():
                if hasattr(sub_subclass, "MODE_INFORMATION_TYPE"):
                    PortModeInformationFormat.__implementations__[sub_subclass.MODE_INFORMATION_TYPE.value] = sub_subclass


class PortModeInformationFormat:
    __implementations__ = None

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        if PortModeInformationFormat.__implementations__ is None:
            build_index()

        mode = message_bytes[0:1]
        mode_information_type = PortModeInformationType(message_bytes[1:2])

        if not PortModeInformationFormat.__implementations__.__contains__(mode_information_type.value):
            raise ProtocolError(f"Unknown port mode information type: {mode_information_type}")

        implementation = PortModeInformationFormat.__implementations__[mode_information_type.value]
        return implementation.parse_bytes(mode, message_bytes[2:])

    @classmethod
    def validate(cls, message_bytes: bytes, max_length: int = None, expected_length: int = None):
        message_length = len(message_bytes)
        if expected_length and message_length != expected_length:
            message = 'Message length: {length} is different from expected length: {expected}. For type: {typename}' \
                .format(length=message_length, expected=expected_length, typename=cls.MODE_INFORMATION_TYPE.name)
            raise ProtocolError(message)
        if max_length and message_length > max_length:
            message = 'Message length: {length} is larger than allowed length of: {expected}. For type: {typename}' \
                .format(length=message_length, expected=max_length, typename=cls.MODE_INFORMATION_TYPE.name)
            raise ProtocolError(message)

    def __init__(self, mode):
        self.mode = mode

    @property
    def value(self):
        return self.mode + self.MODE_INFORMATION_TYPE.value


class PortModeInformationName(PortModeInformationFormat):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.NAME)

    MAX_LENGTH = 11

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, max_length=cls.MAX_LENGTH)

        name = ""

        for char_int_value in message_bytes:
            if not ((48 <= char_int_value <= 57) or (65 <= char_int_value <= 90) or (
                    97 <= char_int_value <= 122) or char_int_value == 95):
                raise ProtocolError(f"Name contains unsupported characters: {chr(char_int_value)}")

            name += chr(char_int_value)

        return PortModeInformationName(mode, name)

    def __init__(self, mode, name):
        super().__init__(mode)
        self.name = name

    @property
    def value(self):
        return super().value + bytes(self.name, 'UTF-8')


class PortModeInformationFloatingPointValues(PortModeInformationFormat):
    EXPECTED_LENGTH = 8

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, expected_length=cls.EXPECTED_LENGTH)

        try:
            min_value = struct.unpack(">f", message_bytes[0:4])[0]
        except Exception as e:
            raise ProtocolError(f"Unable to unpack min value: '{message_bytes[0:4].hex()}' to 4 byte float. Message: {e}")

        try:
            max_value = struct.unpack(">f", message_bytes[4:])[0]
        except Exception as e:
            raise ProtocolError(f"Unable to unpack max value: '{message_bytes[4].hex()}' to 4 byte float. Message: {e}")

        return cls(mode, min_value, max_value)

    def __init__(self, mode, min_value, max_value):
        super().__init__(mode)
        self.min_value = min_value
        self.max_value = max_value

    @property
    def value(self):
        min_value = struct.pack(">f", self.min_value)
        max_value = struct.pack(">f", self.max_value)
        return super().value + min_value + max_value


class PortModeInformationRawRange(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.RAW)


class PortModeInformationPercentageRange(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.PERCENTAGE)


class PortModeInformationSiRange(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.SI)


class PortModeInformationSymbol(PortModeInformationFormat):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.SYMBOL)

    MAX_LENGTH = 5

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, max_length=cls.MAX_LENGTH)

        symbol = ""

        for char_int_value in message_bytes:
            symbol += chr(char_int_value)

        return PortModeInformationSymbol(mode, symbol)

    def __init__(self, mode, symbol):
        super().__init__(mode)
        self.symbol = symbol

    @property
    def value(self):
        return super().value + bytes(self.symbol, 'UTF-8')


class PortModeInformationMapping(PortModeInformationFormat):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.MAPPING)

    EXPECTED_LENGTH = 2

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, expected_length=cls.EXPECTED_LENGTH)

        input_mapping = PortModeMapping.parse_bytes(message_bytes[0:1])
        output_mapping = PortModeMapping.parse_bytes(message_bytes[1:])

        return PortModeInformationMapping(mode, input_mapping, output_mapping)

    def __init__(self, mode: bytes, input_mapping: PortModeMapping, output_mapping: PortModeMapping):
        super().__init__(mode)

        self.input_mapping = input_mapping
        self.output_mapping = output_mapping

    @property
    def value(self):
        return super().value + self.input_mapping.value + self.output_mapping.value


class PortModeInformation(Message):
    MESSAGE_TYPE = MessageType.PORT_MODE_INFO

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length < 4:
            raise ProtocolError("Expected length of at least 4 bytes for message payload.")

        port_id = PortID(message_bytes[0:1])
        information_format = PortModeInformationFormat.parse_bytes(message_bytes[1:])

        return PortModeInformation(port_id, information_format)

    def __init__(self, port_id, information_format):
        self.port_id = port_id
        self.mode_information_type = information_format.MODE_INFORMATION_TYPE
        self.mode_information = information_format

    @property
    def value(self):
        mode_information_bytes = self.mode_information.value
        header = CommonMessageHeader(len(mode_information_bytes)+1, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + mode_information_bytes

