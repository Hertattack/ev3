from src.poweredup.protocol import ProtocolError
from src.poweredup.protocol.messages import Message
from src.poweredup.protocol.ports import PortModeInformation


def test_port_mode_information_name_message_is_supported():
    # header, port id, mode, type, name
    message_bytes = b'\x09\x00\x44\x01\x00\x00\x48\x45\x4C\x4C\x4F'
    message = Message.parse_bytes(message_bytes)
    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "NAME"
    assert message.mode_information.name == "HELLO"


def test_port_mode_information_name_message_validates_length():
    # header, port id, mode, type, name
    message_bytes = b'\x09\x00\x44\x01\x00\x00\x48\x45\x4C\x4C\x4F\x48\x45\x4C\x4C\x4F\x48\x45\x4C\x4C\x4F'
    try:
        message = Message.parse_bytes(message_bytes)
    except ProtocolError as protocolError:
        assert protocolError.message == "Message length: 15 is larger than allowed length of: 11. For type: NAME"


def test_port_mode_information_name_message_validates_allowed_characters():
    # header, port id, mode, type, name
    message_bytes = b'\x09\x00\x44\x01\x00\x00\x48\x45\x4C\x60\x4C\x4F'
    try:
        message = Message.parse_bytes(message_bytes)
    except ProtocolError as protocolError:
        assert protocolError.message == 'Name contains unsupported characters: `'

