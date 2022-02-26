from . import ValueMapping
from messages import Message, CommonMessageHeader, MessageType


class PortID:
    def __init__(self, id_input):
        id_type = type(id_input)

        id_value = None
        if id_type == bytes:
            id_value = int.from_bytes(id_input, byteorder="big", signed=False)
        if id_type == int:
            id_value = id_input

        if id_value is None:
            raise f"Unsupported id type supplied is not supported: {id_type}"

        if 0 > id_value > 255:
            raise f"Expected id value between 0 and 255, but was {id_value}"

        self.value = id_value.to_bytes(1, byteorder="big", signed=False)
        self.id = id_value


class InformationType(ValueMapping):
    PORT_VALUE = b'\x00'
    MODE_INFO = b'\x01'
    POSSIBLE_MODE_COMBINATIONS = b'\x02'


class PortInformationRequestMessage(Message):
    MESSAGE_TYPE = MessageType.PORT_INFO_REQ

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 2:
            raise f"Message length different from expected length (2) = {message_length}"

        return PortInformationRequestMessage(PortID(message_bytes[0:1]), InformationType(message_bytes[1:]))

    def __init__(self, port_id: PortID, information_type: InformationType):
        self.port_id = port_id
        self.information_type = information_type

    @property
    def value(self):
        header = CommonMessageHeader(2, PortInformationRequestMessage.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.information_type.value
