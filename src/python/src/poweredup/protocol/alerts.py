from . import ValueMapping, MessageType, CommonMessageHeader


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


class Alert:

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
