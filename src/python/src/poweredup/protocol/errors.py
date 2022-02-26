from . import ValueMapping
from .messages import MessageType


class ErrorCode(ValueMapping):
    ACK_ERROR = b'\x01'
    MACK_ERROR = b'\x02'
    BUFFER_OVERFLOW = b'\x03'
    TIMEOUT = b'\x04'
    COMMAND_NOT_RECOGNIZED = b'\x05'
    INVALID_USE = b'\x06'
    OVERCURRENT = b'\x07'
    INTERNAL_ERROR = b'\x08'

class ErrorMessage:

    @classmethod
    def parse_bytes(cls, input_bytes: bytes):


    def __init__(self, message_type: bytes, error_code: ErrorCode):
        self.error_code = error_code
        if error_code.value == ErrorCode.COMMAND_NOT_RECOGNIZED:
            self.message_type = None
            self.message_type_raw = message_type
        else:
            self.message_type = MessageType(message_type)
