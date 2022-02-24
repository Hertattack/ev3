SERVICE_UUID = "00001623 -1212-EFDE-1623-785FEABCD123"
CHARACTERISTIC_UUID = "00001624 -1212-EFDE-1623-785FEABCD123"


class LegoWireless:

    def __init__(self):
        pass


class MessageTypes:
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


class HubPropertyOperations:
    SET = b'\x01'
    ENABLE_UPDATES = b'\x02'
    DISABLE_UPDATES = b'\x03'
    RESET = b'\x04'
    REQUEST_UPDATE = b'\x05'
    UPDATE = b'\x06'


"""
Common Header for all messages

Size = 3 bytes.
"""


class CommonMessageHeader:
    HUB_ID = b'\x00'

    def __init__(self, messageLength, messageType):
        self.messageLength = messageLength
        self.messageType = messageType

    def getValue(self):
        actualLength = self.messageLength + 3
        if actualLength <= 127:
            return actualLength.to_bytes(1, byteorder="big", signed=False) + \
                   CommonMessageHeader.HUB_ID + \
                   self.messageType
        else:
            actualLength = actualLength + 1
            remainder = actualLength % 127
            multiplier = (actualLength - remainder) // 127
            return (remainder + 127).to_bytes(1, byteorder='big', signed=False) + multiplier.to_bytes(1,
                                                                                                      byteorder='big',
                                                                                                      signed=False) + CommonMessageHeader.HUB_ID + self.messageType


class VersionNumberEncoding:
    def __init__(self, major, minor, patch, build):
        if 0 <= major <= 7 and 0 <= minor <= 9 and 0 <= patch <= 99 and 0 <= build <= 9999:
            self.major = major
            self.minor = minor
            self.patch = patch
            self.build = build
        else:
            raise f"Unsupported version number. 0 <= {major} <= 7, 0 <= {minor} 9, 0 <= {patch} 99, 0 <= {build} <= 9999"

    def getValue(self):
        return int(f"{self.major}{self.minor}", 16).to_bytes(1, byteorder="big") + \
               int(f"{self.patch}", 16).to_bytes(1, byteorder="big") + \
               int(f"{self.build}", 16).to_bytes(2, byteorder="big")


class LWPVersionNumberEncoding:
    def __init__(self, major, minor):
        if 0 <= major <= 99 and 0 <= minor <= 99:
            self.major = major
            self.minor = minor
        else:
            raise f"Unsupported version number. 0 <= {major} <= 99, 0 <= {minor} 99"

    def getValue(self):
        return int(f"{self.major}{self.minor}", 16).to_bytes(2, byteorder="big")


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
        HubPropertyOperations.SET, HubPropertyOperations.ENABLE_UPDATES,
        HubPropertyOperations.DISABLE_UPDATES, HubPropertyOperations.RESET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

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
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.RESET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

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
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

    def __init__(self, operation, payload):
        if type(payload) != VersionNumberEncoding:
            raise "Expected version number encoding as payload."
        else:
            HubProperty.__init__(self, operation, payload.getValue())


class HWVersionProperty(FWVersionProperty):
    PROPERTY_REF = b'\x04'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class RSSIProperty(HubProperty):
    PROPERTY_REF = b'\x05'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.DISABLE_UPDATES,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

    def __init__(self, operation, value):
        if type(value) != int:
            raise "Only int value type supported"
        if -127 > value > 0:
            raise f"{value} out of range [-127, 0]"
        HubProperty.__init__(operation, value.to_bytes(1, byteorder="big", signed=True))


class BatteryVoltageProperty(HubProperty):
    PROPERTY_REF = b'\x06'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.DISABLE_UPDATES,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

    def __init__(self, operation, percentage):
        if type(percentage) != int or 0 > percentage > 100:
            raise "Expected battery percentage as integer between 0 and 100."

        HubProperty.__init__(self, operation, int.to_bytes(percentage, 1, byteorder="big"))


class BatteryTypeProperty(HubProperty):
    PROPERTY_REF = b'\x07'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

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
        HubPropertyOperations.SET, HubPropertyOperations.ENABLE_UPDATES,
        HubPropertyOperations.DISABLE_UPDATES, HubPropertyOperations.RESET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class RadioFWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x09'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class LegoWirelessProtocolVersionProperty(HubProperty):
    PROPERTY_REF = b'\x0A'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

    def __init__(self, operation, payload):
        if type(payload) != LWPVersionNumberEncoding:
            raise "Expected LWP version number encoding as payload."
        else:
            HubProperty.__init__(self, operation, payload.getValue())


class SystemTypeIDProperty(HubProperty):
    PROPERTY_REF = b'\x0B'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

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
        HubPropertyOperations.SET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class PrimaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0D'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class SecondaryMACProperty(HubProperty):
    PROPERTY_REF = b'\x0E'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class HardwareNWFamilyProperty(HubProperty):
    PROPERTY_REF = b'\x0F'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.SET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]
