import pytest
from src.poweredup.protocol import VersionNumberEncoding


@pytest.mark.parametrize('major, minor, patch, build, expected_outcome', [
    (1, 1, 1, 1, "11010001"),
    (2, 3, 1, 423, "23010423")
])
def test_encoding(major: int, minor: int, patch: int, build: int, expected_outcome: str):
    version = VersionNumberEncoding(major, minor, patch, build)
    assert version.value == int(expected_outcome, 16).to_bytes(4, byteorder="big")


@pytest.mark.parametrize('byte_value, expected_major, expected_minor, expected_patch, expected_build', [
    (b'\x11\x01\x00\x01', 1, 1, 1, 1),
    (b'\x23\x65\x20\x01', 2, 3, 65, 2001),
    (b'\x68\x20\x67\x00', 6, 8, 20, 6700),
    (b'\x10\x00\x00\x00', 1, 0, 0, 0)
])
def test_decoding(byte_value: bytes,
                  expected_major: int, expected_minor: int, expected_patch: int, expected_build: int):
    version = VersionNumberEncoding.parse_bytes(byte_value)
    assert version.value == byte_value
    assert version.major == expected_major
    assert version.minor == expected_minor
    assert version.patch == expected_patch
    assert version.build == expected_build
