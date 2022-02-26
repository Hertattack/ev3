import pytest
from src.poweredup.protocol.messages import MessageType, CommonMessageHeader


@pytest.mark.parametrize('value, expected_pattern', [
    (124, '0b11111110000000001000101'),
    (125, '0b10000001000000010000000001000101'),
    (126, '0b10000010000000010000000001000101')
])
def test_message_header(value: int, expected_pattern: str):
    header = CommonMessageHeader(value, message_type=MessageType.PORT_VALUE_SINGLE)
    assert bin(int.from_bytes(header.value, byteorder="big", signed=False)) == expected_pattern


@pytest.mark.parametrize('header_bytes, expected_length, expected_message_type', [
    (b'\x81\x01\x00\x21', 125, MessageType.PORT_INFO_REQ),
    (b'\x04\x00\x21', 1, MessageType.PORT_INFO_REQ),
    (b'\xaa\xcb\x00\x21', 26022, MessageType.PORT_INFO_REQ)
])
def test_parsing_a_header(header_bytes: bytes, expected_length: int, expected_message_type: bytes):
    header = CommonMessageHeader.parse_bytes(header_bytes)
    assert header.message_length == expected_length
    assert header.message_type.value == expected_message_type
    assert header.value == header_bytes
