from . import VersionNumberEncoding, LWPVersionNumberEncoding, SystemTypeDeviceNumber, ProtocolError, ValueMapping
from .messages import MessageType, CommonMessageHeader, Message


class Operation(ValueMapping):
    SET = b'\x01'
    ENABLE_UPDATES = b'\x02'
    DISABLE_UPDATES = b'\x03'
    RESET = b'\x04'
    REQUEST_UPDATE = b'\x05'
    UPDATE = b'\x06'

    def __init__(self, value: bytes, supported_values):
        if value not in supported_values:
            raise ProtocolError(f"Value: {value.hex()} is not in the list of supported values.")

        ValueMapping.__init__(self, value)


def build_index():
    HubProperty.PROPERTY_IMPLEMENTATIONS = {}
    for subclass in HubProperty.__subclasses__():
        if hasattr(subclass, "PROPERTY_REF"):
            Message.PROPERTY_IMPLEMENTATIONS[subclass.PROPERTY_REF] = subclass


class HubProperty(Message):
    MESSAGE_TYPE = MessageType.HUB_PROPERTY

    PROPERTY_IMPLEMENTATIONS = None

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        if HubProperty.PROPERTY_IMPLEMENTATIONS is None:
            build_index()

        payload_length = len(message_bytes) - 2

        property_type = message_bytes[0:1]

        if not HubProperty.PROPERTY_IMPLEMENTATIONS.__contains__(property_type):
            raise ProtocolError(f"Unknown property type: {property_type}")

        implementation = Message.PROPERTY_IMPLEMENTATIONS[property_type]
        operation = Operation(message_bytes[1:2], implementation.SUPPORTED_OPERATIONS)
        return implementation.parse_bytes(operation, message_bytes[2:] if payload_length > 0 else None)

    def __init__(self, operation: Operation):
        self.operation = operation

    @property
    def value(self):
        header = CommonMessageHeader(2, MessageType.HUB_PROPERTY)
        return header.value + self.PROPERTY_REF + self.operation


class AdvertisingNameProperty(HubProperty):
    PROPERTY_REF = b'\x01'
    SUPPORTED_OPERATIONS = [
        Operation.SET, Operation.ENABLE_UPDATES,
        Operation.DISABLE_UPDATES, Operation.RESET,
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    MIN_SIZE = 1
    MAX_SIZE = 14

    def __init__(self, operation: Operation, name: str):
        if type(name) != str:
            raise ProtocolError("Expected name as string.")

        payload = bytes(name, 'utf8')

        HubProperty.__init__(self, operation)


class ButtonProperty(HubProperty):
    PROPERTY_REF = b'\x02'
    SUPPORTED_OPERATIONS = [
        Operation.ENABLE_UPDATES, Operation.RESET,
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    TRUE = b'\x00'
    FALSE = b'\x01'

    def __init__(self, operation: Operation, payload: bytes):
        if payload == ButtonProperty.TRUE or payload == ButtonProperty.TRUE:
            HubProperty.__init__(self, operation, payload)
        else:
            raise ProtocolError("Button value is not within range.")


class FWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x03'

    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    def __init__(self, operation: Operation, payload: bytes):
        if type(payload) != VersionNumberEncoding:
            raise ProtocolError("Expected version number encoding as payload.")
        else:
            HubProperty.__init__(self, operation, payload.value)


class HWVersionProperty(FWVersionProperty):
    PROPERTY_REF = b'\x04'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class RSSIProperty(HubProperty):
    PROPERTY_REF = b'\x05'
    SUPPORTED_OPERATIONS = [
        Operation.ENABLE_UPDATES, Operation.DISABLE_UPDATES,
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    def __init__(self, operation: Operation, value: bytes):
        if type(value) != int:
            raise ProtocolError("Only int value type supported")
        if -127 > value > 0:
            raise ProtocolError(f"{value} out of range [-127, 0]")

        HubProperty.__init__(operation, value.to_bytes(1, byteorder="big", signed=True))


class BatteryVoltageProperty(HubProperty):
    PROPERTY_REF = b'\x06'
    SUPPORTED_OPERATIONS = [
        Operation.ENABLE_UPDATES, Operation.DISABLE_UPDATES,
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    def __init__(self, operation: Operation, percentage: bytes):
        if type(percentage) != int or 0 > percentage > 100:
            raise ProtocolError("Expected battery percentage as integer between 0 and 100.")

        HubProperty.__init__(self, operation, int.to_bytes(percentage, 1, byteorder="big"))


class BatteryTypeProperty(HubProperty):
    PROPERTY_REF = b'\x07'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    NORMAL = b'\x00'
    RECHARGEABLE = b'\x01'

    def __init__(self, operation: Operation, payload: bytes):
        if payload == BatteryTypeProperty.NORMAL or payload == BatteryTypeProperty.RECHARGEABLE:
            HubProperty.__init__(self, operation, payload)
        else:
            raise ProtocolError("Battery type is not within range.")


class ManufacturerNameProperty(HubProperty):
    PROPERTY_REF = b'\x08'
    SUPPORTED_OPERATIONS = [
        Operation.SET, Operation.ENABLE_UPDATES,
        Operation.DISABLE_UPDATES, Operation.RESET,
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class RadioFWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x09'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class LegoWirelessProtocolVersionProperty(HubProperty):
    PROPERTY_REF = b'\x0A'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    def __init__(self, operation: Operation, payload: LWPVersionNumberEncoding):
        HubProperty.__init__(self, operation, payload.value)


class SystemTypeIDProperty(HubProperty):
    PROPERTY_REF = b'\x0B'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]

    def __init__(self, operation, system_type: SystemTypeDeviceNumber):
        HubProperty.__init__(self, operation, system_type.value)


class HWNetworkIDProperty(HubProperty):
    PROPERTY_REF = b'\x0C'
    SUPPORTED_OPERATIONS = [
        Operation.SET,
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class PrimaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0D'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class SecondaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0E'
    SUPPORTED_OPERATIONS = [
        Operation.REQUEST_UPDATE, Operation.UPDATE]


class HardwareNWFamilyProperty(HubProperty):
    PROPERTY_REF = b'\x0F'
    SUPPORTED_OPERATIONS = [
        Operation.SET,
        Operation.REQUEST_UPDATE, Operation.UPDATE]
