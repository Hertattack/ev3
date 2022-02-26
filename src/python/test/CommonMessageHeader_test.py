from src.poweredup.protocol import CommonMessageHeader, MessageTypes
import pytest

@pytest.mark.parametrize('value, expected_pattern', [
    (124, '0b11111110000000001000101'),
    (125, '0b10000001000000010000000001000101'),
    (126, '0b10000010000000010000000001000101')
])
def test_message_header(value: int, expected_pattern: str):
    header = CommonMessageHeader(value, message_type=MessageTypes.PORT_VALUE_SINGLE)
    assert bin(int.from_bytes(header.value, byteorder="big", signed=False)) == expected_pattern
