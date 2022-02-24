import pytest
from src.poweredup.protocol import VersionNumberEncoding


@pytest.mark.parametrize('major, minor, patch, build, expectedOutcome', [
    (1, 1, 1, 1, "11010001")
])
def test_encoding(major, minor, patch, build, expectedOutcome):
    version = VersionNumberEncoding(major, minor, patch, build)
    assert version.getValue() == int(expectedOutcome, 16).to_bytes(4, byteorder="big")
