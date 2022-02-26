from src.poweredup.protocol.properties import Operations, FWVersionProperty
from src.poweredup.protocol import VersionNumberEncoding


def test_getValue():
    v = VersionNumberEncoding(1, 2, 3, 4)
    p = FWVersionProperty(Operations.REQUEST_UPDATE, v)
    assert p.getValue() == b'\t\x00\x01\x03\x05\x12\x03\x00\x04'
