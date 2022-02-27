from . import ValueMapping, ProtocolError
from .messages import MessageType, CommonMessageHeader, Message


class AlertType(ValueMapping):
    LOW_VOLTAGE = b'\x01'
    HIGH_CURRENT = b'\x02'
    LOW_SIGNAL_STRENGTH = b'\x03'
    OVER_POWER_CONDITION = b'\x04'


class AlertOperation(ValueMapping):
    ENABLE_UPDATES = b'\x01'
    DISABLE_UPDATES = b'\x02'
    REQUEST_UPDATES = b'\x03'
    UPDATE = b'\x04'


class AlertStatus(ValueMapping):
    OK = b'\x00'
    ALERT = b'\xFF'


class AlertMessage(Message):
    MESSAGE_TYPE = MessageType.HUB_ALERT

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if 2 > message_length > 3:
            raise ProtocolError(f"Expected message length to be between 5 and 6 bytes, was {message_length}")

        return cls(message_bytes[0:1], message_bytes[1:2], None if message_length == 2 else message_bytes[2:])

    def __init__(self, alert_type: bytes, operation: bytes, payload: bytes = None):
        self.alert_type = AlertType(alert_type)
        self.operation = AlertOperation(operation)
        self.status = None if payload is None else AlertStatus(payload)

    @property
    def value(self):
        length = 2 if self.status is None else 3
        header = CommonMessageHeader(length, MessageType.HUB_ALERT)

        if self.status is None:
            return header.value + self.alert_type.value + self.operation.value
        else:
            return header.value + self.alert_type.value + self.operation.value + self.status.value
