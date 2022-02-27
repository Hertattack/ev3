from src.poweredup.protocol.messages import Message
from src.poweredup.protocol.io import AttachedIoMessage, IOType, EventType


def test_detached_io_message():
    message_bytes = b'\x05\x00\x04\x01\x00'
    message: AttachedIoMessage = Message.parse_bytes(message_bytes)
    assert message.port_id.id == 1
    assert message.event_type == b'\x00'
    assert message == message_bytes


def test_attached_io_message():
    message_bytes = b'\x0F\x00\x04\x02\x01\x00\x14\x12\x03\x35\x78\x21\x14\x00\x32'
    message: AttachedIoMessage = Message.parse_bytes(message_bytes)
    assert message.port_id.id == 2
    assert message.event_type == EventType.ATTACHED_IO
    assert message.attached_io_type == IOType.VOLTAGE
    assert message.hw_revision.major == 1
    assert message.hw_revision.minor == 2
    assert message.hw_revision.patch == 3
    assert message.hw_revision.build == 3578
    assert message.sw_revision.major == 2
    assert message.sw_revision.minor == 1
    assert message.sw_revision.patch == 14
    assert message.sw_revision.build == 32
    assert message == message_bytes


def test_virtual_io_message():
    message_bytes = b'\x09\x00\x04\x11\x02\x00\x17\x15\x23'
    message: AttachedIoMessage = Message.parse_bytes(message_bytes)
    assert message.port_id.id == 17
    assert message.event_type == EventType.VIRTUAL_IO
    assert message.attached_io_type == IOType.RGB_LIGHT
    assert message.port_id_a.id == 21
    assert message.port_id_b.id == 35
    assert message == message_bytes
