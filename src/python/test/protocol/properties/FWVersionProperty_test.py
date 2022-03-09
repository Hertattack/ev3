from src.poweredup.protocol.properties import Operation, FWVersionProperty, HubProperty
from src.poweredup.protocol.messages import Message, CommonMessageHeader
from src.poweredup.protocol import VersionNumberEncoding


def test_value():
    v = VersionNumberEncoding(1, 2, 3, 4)
    message_payload = FWVersionProperty.PROPERTY_REF + Operation.REQUEST_UPDATE + v.value
    header = CommonMessageHeader(len(message_payload), HubProperty.MESSAGE_TYPE)
    p = Message.parse_bytes(header.value + message_payload)
    assert p.value == b'\t\x00\x01\x03\x05\x12\x03\x00\x04'
