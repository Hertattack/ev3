import pytest

from src.poweredup.protocol.actions import ActionType
from src.poweredup.protocol.messages import Message


@pytest.mark.parametrize('action_type, expected_type', [
    (b'\x02', ActionType.DISCONNECT),
    (b'\x05', ActionType.ACTIVATE_BUSY_INDICATION)
])
def test_action_message_parsed_correctly(action_type: bytes, expected_type: bytes):
    message_bytes = b'\x04\x00\x02' + action_type
    action_message = Message.parse_bytes(message_bytes)
    assert action_message.action_type.value == expected_type
