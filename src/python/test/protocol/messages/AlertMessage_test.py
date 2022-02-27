import pytest
from src.poweredup.protocol import ProtocolError
from src.poweredup.protocol.messages import Message, MessageType
from src.poweredup.protocol.alerts import AlertMessage, AlertOperation, AlertStatus


@pytest.mark.parametrize('alert_type, alert_operation, expected_value', [
    (b'\x02', b'\x04', b'\x05\x00\x03\x02\x04'),
    (b'\x04', b'\x04', b'\x05\x00\x03\x04\x04')
])
def test_alert_message_without_payload(alert_type: bytes, alert_operation: bytes, expected_value: bytes):
    message_bytes = b'\x05\x00\x03' + alert_type + alert_operation
    alert_message: AlertMessage = Message.parse_bytes(message_bytes)
    assert alert_message.alert_type.value == alert_type
    assert alert_message.operation.value == alert_operation
    assert alert_message.value == expected_value


def test_alert_message_unsupported_type():
    message_bytes = b'\x05\x00\x03\x44\x04'
    with pytest.raises(ProtocolError, match=r"Value .* is not supported in mapping."):
        Message.parse_bytes(message_bytes)
