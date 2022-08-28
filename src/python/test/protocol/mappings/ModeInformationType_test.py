from src.poweredup.protocol.ports.port_mode_information import ModeInformationType


def test_mode_information_supports_name():
    mode = b'\x00'
    mode_information: ModeInformationType = ModeInformationType(mode)
    assert mode_information.name == 'NAME'
