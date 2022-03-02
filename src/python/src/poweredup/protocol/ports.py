from . import ValueMapping, ProtocolError
from .messages import Message, CommonMessageHeader, MessageType


class PortID:
    def __init__(self, id_input):
        id_type = type(id_input)

        id_value = None
        if id_type == bytes:
            id_value = int.from_bytes(id_input, byteorder="big", signed=False)
        if id_type == int:
            id_value = id_input

        if id_value is None:
            raise ProtocolError(f"Unsupported id type supplied is not supported: {id_type}")

        if 0 > id_value > 255:
            raise ProtocolError(f"Expected id value between 0 and 255, but was {id_value}")

        self.value = id_value.to_bytes(1, byteorder="big", signed=False)
        self.id = id_value


class InformationType(ValueMapping):
    PORT_VALUE = b'\x00'
    MODE_INFO = b'\x01'
    POSSIBLE_MODE_COMBINATIONS = b'\x02'


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


class PortInformationRequestMessage(Message):
    MESSAGE_TYPE = MessageType.PORT_INFO_REQ

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 2:
            raise ProtocolError(f"Message length different from expected length (2) = {message_length}")

        return PortInformationRequestMessage(PortID(message_bytes[0:1]), InformationType(message_bytes[1:]))

    def __init__(self, port_id: PortID, information_type: InformationType):
        self.port_id = port_id
        self.information_type = information_type

    @property
    def value(self):
        header = CommonMessageHeader(2, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.information_type.value


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


class PortInputFormatSetupSingle(Message):
    MESSAGE_TYPE = MessageType.PORT_INPUT_FORMAT_SETUP_SINGLE

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 7:
            raise ProtocolError("Expected length of 6 bytes for message payload.")

        port_id = PortID(message_bytes[0:1])
        mode = message_bytes[1:2]
        delta_interval = message_bytes[2:6]
        notification_enabled = int.from_bytes(message_bytes[6:], byteorder="big", signed=False)

        return PortInputFormatSetupSingle(port_id, mode, delta_interval, notification_enabled)

    def __init__(self, port_id: PortID, mode: bytes, delta_interval: bytes, notification_enabled: int):
        if len(mode) != 1:
            raise ProtocolError("Expected length of mode is 1 bytes.")

        if len(delta_interval) != 4:
            raise ProtocolError("Expected length of delta interval is 4 bytes (uint32)")

        if 0 > notification_enabled > 1:
            raise ProtocolError("Expected notification value to be 0 = Disabled and 1 = Enabled")

        self.port_id = port_id
        self.mode = mode
        self.delta_interval = delta_interval
        self.notification_enabled = notification_enabled

    @property
    def value(self):
        header = CommonMessageHeader(7, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.mode + self.delta_interval + \
               self.notification_enabled.to_bytes(1, byteorder="big", signed=False)


class PortInputFormatSetupCombined(Message):
    MESSAGE_TYPE = MessageType.PORT_INPUT_FORMAT_SETUP_COMBINED

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        pass

    def __init__(self):
        pass

    @property
    def value(self):
        pass
