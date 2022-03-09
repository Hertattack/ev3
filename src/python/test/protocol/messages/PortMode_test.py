import pytest
from src.poweredup.protocol.ports import PortModes


@pytest.mark.parametrize('value, expected_modes', [
    (b'\x00\x01', ['mode_0']),
    (b'D\x11', ['mode_0', 'mode_4', 'mode_10', 'mode_14'])
])
def test_port_modes(value, expected_modes):
    modes = PortModes(value)
    selected_modes = []
    for attr_name in dir(modes):
        if attr_name.startswith("mode"):
            if getattr(modes, attr_name):
                selected_modes.append(attr_name)

    assert len(selected_modes) == len(expected_modes)

    for expected_mode in expected_modes:
        assert selected_modes.__contains__(expected_mode)
