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
            return actualLength.to_bytes(1, byteorder="big",
                                         signed=False) + CommonMessageHeader.HUB_ID + self.messageType
        else:
            actualLength = actualLength + 1
            remainder = actualLength % 127
            multiplier = (actualLength - remainder) // 127
            return (remainder + 127).to_bytes(1, byteorder='big', signed=False) + multiplier.to_bytes(1,
                                                                                                      byteorder='big',
                                                                                                      signed=False) + CommonMessageHeader.HUB_ID + self.messageType


class HubProperty:
    def getValue(self):
        header = CommonMessageHeader(2, MessageTypes.HUB_PROPERTY)
        return header.getValue() + self.PROPERTY_REF + self.operation

    def __init__(self, operation, payload):
        if operation in self.SUPPORTED_OPERATIONS:
            self.operation = operation
            self.payload = payload
        else:
            raise f"Operation: {operation.hex()} not supported."


class AdvertisingNameProperty(HubProperty):
    PROPERTY_REF = b'\x01'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.SET, HubPropertyOperations.ENABLE_UPDATES,
        HubPropertyOperations.DISABLE_UPDATES, HubPropertyOperations.RESET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]

    MIN_SIZE = 1
    MAX_SIZE = 14

    def __init__(self, operation, payload):
        # pad payload to MAX_SIZE
        paddedPayload = payload
        HubProperty.__init__(self, operation, paddedPayload)


class ButtonProperty(HubProperty):
    PROPERTY_REF = b'\x02'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.RESET,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class FWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x03'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class HWVersionProperty(HubProperty):
    PROPERTY_REF = b'\x04'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class RSSIProperty(HubProperty):
    PROPERTY_REF = b'\x05'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.DISABLE_UPDATES,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class BatteryVoltageProperty(HubProperty):
    PROPERTY_REF = b'\x06'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.ENABLE_UPDATES, HubPropertyOperations.DISABLE_UPDATES,
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


class BatteryTypeProperty(HubProperty):
    PROPERTY_REF = b'\x07'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


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


class SystemTypeIDProperty(HubProperty):
    PROPERTY_REF = b'\x0B'
    SUPPORTED_OPERATIONS = [
        HubPropertyOperations.REQUEST_UPDATE, HubPropertyOperations.UPDATE]


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
