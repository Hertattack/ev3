from src.poweredup.protocol.ports.port_mode_information import PortModeMapping


def test_port_mode_mapping_is_supported():
    value = b'\x58'
    mapping = PortModeMapping.parse_bytes(value)
    assert mapping.value.hex() == value.hex()
