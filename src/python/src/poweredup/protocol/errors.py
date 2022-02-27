from . import ValueMapping
from .messages import Message, MessageType


class ErrorCode(ValueMapping):
    ACK_ERROR = b'\x01'
    MACK_ERROR = b'\x02'
    BUFFER_OVERFLOW = b'\x03'
    TIMEOUT = b'\x04'
    COMMAND_NOT_RECOGNIZED = b'\x05'
    INVALID_USE = b'\x06'
    OVERCURRENT = b'\x07'
    INTERNAL_ERROR = b'\x08'


class ErrorMessage(Message):
    MESSAGE_TYPE = MessageType.GENERIC_ERROR_MSG

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 2:
            raise ProtocolError(f"Message length {message_length} differs from expected length: 2")

        return ErrorMessage(message_bytes[0:1], ErrorCode(message_bytes[1:]))

    def __init__(self, message_type: bytes, error_code: ErrorCode):
        self.error_code = error_code
        if error_code.value == ErrorCode.COMMAND_NOT_RECOGNIZED:
            self.message_type = None
            self.message_type_raw = message_type
        else:
            self.message_type = MessageType(message_type)
