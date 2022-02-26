from src.poweredup.protocol.alerts import Alert, AlertOperation, AlertType, AlertStatus


def test_alert_downstream_encoding():
    alert = Alert(AlertType.LOW_SIGNAL_STRENGTH, AlertOperation.ENABLE_UPDATES)
    assert alert.value == b'\x05\x00\x03\x03\x01'


def test_alert_upstream_encoding():
    alert = Alert(AlertType.LOW_SIGNAL_STRENGTH, AlertOperation.ENABLE_UPDATES, AlertStatus.ALERT)
    assert alert.value == b'\x06\x00\x03\x03\x01\xFF'
