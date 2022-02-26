import pytest
from src.poweredup.protocol import VersionNumberEncoding


@pytest.mark.parametrize('major, minor, patch, build, expected_outcome', [
    (1, 1, 1, 1, "11010001")
])
def test_encoding(major: int, minor: int, patch: int, build: int, expected_outcome: str):
    version = VersionNumberEncoding(major, minor, patch, build)
    assert version.value == int(expected_outcome, 16).to_bytes(4, byteorder="big")
