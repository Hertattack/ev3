from src.poweredup.protocol import ValueMapping


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

    Size = 3 bytes or 4 bytes depending on the length of the message.
    """
    HUB_ID = b'\x00'

    REMAINDER_MASK = int("01111111", 2)

    @classmethod
    def parse_bytes(cls, message_header_bytes: bytes):
        header_length = len(message_header_bytes)
        if 3 > header_length > 4:
            raise f"Unsupported header length {header_length}"

        message_type = message_header_bytes[header_length - 1]

        if header_length == 3:
            message_length = int.from_bytes(message_header_bytes[0:1], byteorder="big", signed=False) - header_length
            return CommonMessageHeader(message_length, message_header_bytes[2:3])

        multiplier = int.from_bytes(message_header_bytes[1:2], byteorder="big", signed=False)
        remainder = int.from_bytes(message_header_bytes[0:1], byteorder="big",
                                   signed=False) & CommonMessageHeader.REMAINDER_MASK
        message_length = multiplier * 128 + remainder - header_length
        return CommonMessageHeader(message_length, message_header_bytes[3:])

    def __init__(self, message_length: int, message_type: bytes):
        self.message_length = message_length
        self.message_type = MessageType(message_type)

    @property
    def value(self):
        if self.message_length + 3 <= 127:
            actual_length = self.message_length + 3
            return actual_length.to_bytes(1, byteorder="big", signed=False) + \
                   CommonMessageHeader.HUB_ID + \
                   self.message_type.value
        else:
            actual_length = self.message_length + 4
            remainder = actual_length % 128
            multiplier = (actual_length - remainder) // 128
            return (remainder + 128).to_bytes(1, byteorder='big', signed=False) + \
                   multiplier.to_bytes(1, byteorder='big', signed=False) + \
                   CommonMessageHeader.HUB_ID + self.message_type.value


def build_index():
    Message.IMPLEMENTATIONS = {}
    for subclass in Message.__subclasses__():
        if hasattr(subclass, "MESSAGE_TYPE"):
            Message.IMPLEMENTATIONS[subclass.MESSAGE_TYPE] = subclass


class Message:
    IMPLEMENTATIONS = None

    LENGTH_MASK = int("10000000", 2)

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        if Message.IMPLEMENTATIONS is None:
            build_index()

        header_length = 3
        if (message_bytes[0] & Message.LENGTH_MASK) == 128:
            header_length = 4

        header: CommonMessageHeader = CommonMessageHeader.parse_bytes(message_bytes[0:header_length])
        if not Message.IMPLEMENTATIONS.__contains__(header.message_type.value):
            raise f"Unknown message type: {header.message_type.name}"

        implementation = Message.IMPLEMENTATIONS[header.message_type.value]
        return implementation.parse_bytes(message_bytes[header_length:])

    def __eq__(self, other):
        self_has_value = "value" in dir(self)
        if type(self) == type(other):
            if self_has_value:
                return self.value == other.value
            else:
                return self is other
        elif type(other) == bytes:
            if self_has_value:
                return self.value == other
            else:
                return False

        return False
