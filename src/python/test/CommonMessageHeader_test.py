from src.poweredup.protocol import CommonMessageHeader, MessageTypes
import pytest

@pytest.mark.parametrize('value,expectedPattern', [
    (124, '0b11111110000000001000101'),
    (125, '0b10000001000000010000000001000101'),
    (126, '0b10000010000000010000000001000101')
])
def test_messageheader(value, expectedPattern):
    header = CommonMessageHeader(value, messageType=MessageTypes.PORT_VALUE_SINGLE)
    assert bin(int.from_bytes(header.getValue(), byteorder="big", signed=False)) == expectedPattern