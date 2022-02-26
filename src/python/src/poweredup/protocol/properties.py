from src.poweredup.protocol import CommonMessageHeader, MessageTypes, VersionNumberEncoding, LWPVersionNumberEncoding


class Operations:
    SET = b'\x01'
    ENABLE_UPDATES = b'\x02'
    DISABLE_UPDATES = b'\x03'
    RESET = b'\x04'
    REQUEST_UPDATE = b'\x05'
    UPDATE = b'\x06'


class HubProperty:
    def __init__(self, operation, payload):
        payloadType = type(payload)
        if payloadType == bytes:
            self.payload = payload
        elif payloadType == bytearray:
            self.payload = bytes(payload)
        elif payloadType == str:
            self.payload = bytes(payload, 'utf8')
        else:
            raise f"Unsupported payload type: {payloadType}"

        if operation in self.SUPPORTED_OPERATIONS:
            self.operation = operation
            self.payload = payload
        else:
            raise f"Operation: {operation.hex()} not supported."

    def validatePayloadLength(self, payload):
        if len(self.payload) > self.MAX_SIZE:
            raise f"Payload exceeds maximum size: {self.MAX_SIZE}"
        elif len(self.payload) < self.MIN_SIZE:
            raise f"Payload under minimum size: {self.MIN_SIZE}"
        else:
            return True

    def getValue(self):
        header = CommonMessageHeader(len(self.payload) + len(self.PROPERTY_REF) + len(self.operation),
                                     MessageTypes.HUB_PROPERTY)
        return header.getValue() + self.PROPERTY_REF + self.operation + self.payload


class AdvertisingNameProperty(HubProperty):
    PROPERTY_REF = b'\x01'
    SUPPORTED_OPERATIONS = [
        Operations.SET, Operations.ENABLE_UPDATES,
        Operations.DISABLE_UPDATES, Operations.RESET,
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    def __init__(self, operation, name):
        if type(name) != str:
            raise "Expected name as string."

        payload = bytes(name, 'utf8')
        if 1 > len(payload) > 14:
            raise "Name should be between 1 and 14 characters."

        HubProperty.__init__(self, operation, payload)


class ButtonProperty(HubProperty):
    PROPERTY_REF = b'\x02'
    SUPPORTED_OPERATIONS = [
        Operations.ENABLE_UPDATES, Operations.RESET,
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    TRUE = b'\x00'
    FALSE = b'\x01'

    def __init__(self, operation, payload):
        if payload == ButtonProperty.TRUE or payload == ButtonProperty.TRUE:
            HubProperty.__init__(self, operation, payload)
        else:
            raise "Button value is not within range."


class FWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x03'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    def __init__(self, operation, payload):
        if type(payload) != VersionNumberEncoding:
            raise "Expected version number encoding as payload."
        else:
            HubProperty.__init__(self, operation, payload.getValue())


class HWVersionProperty(FWVersionProperty):
    PROPERTY_REF = b'\x04'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class RSSIProperty(HubProperty):
    PROPERTY_REF = b'\x05'
    SUPPORTED_OPERATIONS = [
        Operations.ENABLE_UPDATES, Operations.DISABLE_UPDATES,
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    def __init__(self, operation, value):
        if type(value) != int:
            raise "Only int value type supported"
        if -127 > value > 0:
            raise f"{value} out of range [-127, 0]"
        HubProperty.__init__(operation, value.to_bytes(1, byteorder="big", signed=True))


class BatteryVoltageProperty(HubProperty):
    PROPERTY_REF = b'\x06'
    SUPPORTED_OPERATIONS = [
        Operations.ENABLE_UPDATES, Operations.DISABLE_UPDATES,
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    def __init__(self, operation, percentage):
        if type(percentage) != int or 0 > percentage > 100:
            raise "Expected battery percentage as integer between 0 and 100."

        HubProperty.__init__(self, operation, int.to_bytes(percentage, 1, byteorder="big"))


class BatteryTypeProperty(HubProperty):
    PROPERTY_REF = b'\x07'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    NORMAL = b'\x00'
    RECHARGEABLE = b'\x01'

    def __init__(self, operation, payload):
        if payload == BatteryTypeProperty.NORMAL or payload == BatteryTypeProperty.RECHARGEABLE:
            HubProperty.__init__(self, operation, payload)
        else:
            raise "Battery type is not within range."


class ManufacturerNameProperty(HubProperty):
    PROPERTY_REF = b'\x08'
    SUPPORTED_OPERATIONS = [
        Operations.SET, Operations.ENABLE_UPDATES,
        Operations.DISABLE_UPDATES, Operations.RESET,
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class RadioFWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x09'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class LegoWirelessProtocolVersionProperty(HubProperty):
    PROPERTY_REF = b'\x0A'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    def __init__(self, operation, payload):
        if type(payload) != LWPVersionNumberEncoding:
            raise "Expected LWP version number encoding as payload."
        else:
            HubProperty.__init__(self, operation, payload.getValue())


class SystemTypeIDProperty(HubProperty):
    PROPERTY_REF = b'\x0B'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]

    LEGO_WEDO_HUB = '00000000'
    LEGO_DUPLO_TRAIN = '00100000'
    LEGO_BOOST_HUB = '01000000'
    LEGO_2_PORT_HUB = '01000001'
    LEGO_2_PORT_HANDSET = '01000010'

    def __init__(self, operation, systemType):
        if systemType == SystemTypeIDProperty.LEGO_WEDO_HUB or \
                systemType == SystemTypeIDProperty.LEGO_DUPLO_TRAIN or \
                systemType == SystemTypeIDProperty.LEGO_BOOST_HUB or \
                systemType == SystemTypeIDProperty.LEGO_2_PORT_HUB or \
                systemType == SystemTypeIDProperty.LEGO_2_PORT_HANDSET:
            HubProperty.__init__(self, operation, int(systemType, 2).to_bytes(1, byteorder="big"))
        else:
            raise "Unsupported system type."


class HWNetworkIDProperty(HubProperty):
    PROPERTY_REF = b'\x0C'
    SUPPORTED_OPERATIONS = [
        Operations.SET,
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class PrimaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0D'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class SecondaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0E'
    SUPPORTED_OPERATIONS = [
        Operations.REQUEST_UPDATE, Operations.UPDATE]


class HardwareNWFamilyProperty(HubProperty):
    PROPERTY_REF = b'\x0F'
    SUPPORTED_OPERATIONS = [
        Operations.SET,
        Operations.REQUEST_UPDATE, Operations.UPDATE]