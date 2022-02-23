from src.poweredup.protocol import HubPropertyOperations, FWVersionProperty


def test_getValue():
    p = FWVersionProperty(HubPropertyOperations.REQUEST_UPDATE, 0)
    assert p.getValue() == b'\x05\x00\x01\x03\x05'
