from src.poweredup.protocol import HubPropertyOperations, FWVersionProperty, VersionNumberEncoding


def test_getValue():
    v = VersionNumberEncoding(1, 2, 3, 4)
    p = FWVersionProperty(HubPropertyOperations.REQUEST_UPDATE, v)
    assert p.getValue() == b'\t\x00\x01\x03\x05\x12\x03\x00\x04'
