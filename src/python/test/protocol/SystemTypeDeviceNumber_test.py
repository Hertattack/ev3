import pytest
from src.poweredup.protocol import SystemTypeDeviceNumber

LEGO_WEDO_HUB = b'\x00'
LEGO_DUPLO_TRAIN = b'\x20'
LEGO_BOOST_HUB = b'\x40'
LEGO_2_PORT_HUB = b'\x41'
LEGO_2_PORT_HANDSET = b'\x42'


@pytest.mark.parametrize('system_type, expected_outcome', [
    (LEGO_WEDO_HUB, "LEGO_WEDO_HUB"),
    (LEGO_DUPLO_TRAIN, "LEGO_DUPLO_TRAIN"),
    (LEGO_BOOST_HUB, "LEGO_BOOST_HUB"),
    (LEGO_2_PORT_HUB, "LEGO_2_PORT_HUB"),
    (LEGO_2_PORT_HANDSET, "LEGO_2_PORT_HANDSET")
])
def test_initialization(system_type: bytes, expected_outcome: str):
    system_type_device_no = SystemTypeDeviceNumber(system_type)
    assert system_type_device_no.name == expected_outcome
