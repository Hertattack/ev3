from src.poweredup.protocol.messages import Message
from src.poweredup.protocol.ports import PortInformation


def test_mode_combination_supported():
    message_bytes = b'\x09\x00\x43\x0F\x02\x11\x11\x00\x01'
    message = Message.parse_bytes(message_bytes)
    assert message.value == message_bytes
