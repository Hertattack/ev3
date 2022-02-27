from . import ValueMapping, VersionNumberEncoding, ProtocolError
from .messages import MessageType, CommonMessageHeader, Message
from .ports import PortID


class EventType(ValueMapping):
    DETACHED_IO = b'\x00'
    ATTACHED_IO = b'\x01'
    VIRTUAL_IO = b'\x02'


class IOType(ValueMapping):
    MOTOR = b'\x00\x01'
    TRAIN_MOTOR = b'\x00\x02'
    BUTTON = b'\x00\x05'
    LED_LIGHT = b'\x00\x08'
    VOLTAGE = b'\x00\x14'
    CURRENT = b'\x00\x15'
    PIEZO_TONE = b'\x00\x16'
    RGB_LIGHT = b'\x00\x17'
    EXTERNAL_TILT_SENSOR = b'\x00\x22'
    MOTION_SENSOR = b'\x00\x23'
    VISION_SENSOR = b'\x00\x25'
    EXTERNAL_MOTOR_TACHO = b'\x00\x26'
    INTERNAL_MOTOR_TACHO = b'\x00\x27'
    INTERNAL_TILT = b'\x00\x28'


class AttachedIoMessage(Message):
    MESSAGE_TYPE = MessageType.HUB_ATTACHED_IO

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if 2 > message_length > 12:
            raise ProtocolError(f"Message length of {message_length} out of bounds: 3 - 12")

        port_id = PortID(message_bytes[0:1])
        event_type = EventType(message_bytes[1:2])

        attached_io_type = None if event_type.value == EventType.DETACHED_IO else IOType(message_bytes[2:4])

        hw_revision = None if event_type.value != EventType.ATTACHED_IO else VersionNumberEncoding.parse_bytes(message_bytes[4:8])
        sw_revision = None if event_type.value != EventType.ATTACHED_IO else VersionNumberEncoding.parse_bytes(message_bytes[8:])

        port_id_a = None if event_type.value != EventType.VIRTUAL_IO else PortID(message_bytes[4:5])
        port_id_b = None if event_type.value != EventType.VIRTUAL_IO else PortID(message_bytes[5:])

        return AttachedIoMessage(port_id, event_type, attached_io_type, hw_revision, sw_revision, port_id_a, port_id_b)

    def __init__(self, port_id: PortID, event_type: EventType,
                 attached_io_type: IOType = None,
                 hw_revision: VersionNumberEncoding = None, sw_revision: VersionNumberEncoding = None,
                 port_a_id: PortID = None, port_b_id: PortID = None):

        if event_type.value == EventType.DETACHED_IO and (
                attached_io_type is not None or
                hw_revision is not None or sw_revision is not None or
                port_a_id is not None or port_b_id is not None):
            raise ProtocolError("Unsupported arguments for detached IO.")

        if event_type.value != EventType.DETACHED_IO and attached_io_type is None:
            raise ProtocolError("Expected attached io type to be specified.")

        if event_type.value == EventType.ATTACHED_IO and (port_a_id is not None or port_b_id is not None):
            raise ProtocolError("Port a and b can only be specified for virtual events.")

        if event_type.value == EventType.ATTACHED_IO and (hw_revision is None or sw_revision is None):
            raise ProtocolError("Expected hw and sw revision to be specified for attached io.")

        if event_type.value == EventType.VIRTUAL_IO and (hw_revision is not None or sw_revision is not None):
            raise ProtocolError("Expected hw and sw revision to be none for virtual io.")

        if event_type.value == EventType.VIRTUAL_IO and (port_a_id is None or port_b_id is None):
            raise ProtocolError("Expected port a and b to be set for virtual io.")

        self.port_id = port_id
        self.event_type = event_type

        self.attached_io_type = None if attached_io_type is None else attached_io_type

        self.hw_revision = None if hw_revision is None else hw_revision
        self.sw_revision = None if sw_revision is None else sw_revision

        self.port_id_a = None if port_a_id is None else port_a_id
        self.port_id_b = None if port_b_id is None else port_b_id

    @property
    def value(self):
        if self.event_type == EventType.DETACHED_IO:
            header = CommonMessageHeader(2, MessageType.HUB_ATTACHED_IO)
            return header.value + self.port_id.value + self.event_type.value
        elif self.event_type == EventType.ATTACHED_IO:
            header = CommonMessageHeader(12, MessageType.HUB_ATTACHED_IO)
            return header.value + self.port_id.value + self.event_type.value + \
                   self.attached_io_type.value + \
                   self.hw_revision.value + self.sw_revision.value
        else:
            header = CommonMessageHeader(6, MessageType.HUB_ATTACHED_IO)
            return header.value + self.port_id.value + self.event_type.value + \
                   self.attached_io_type.value + \
                   self.port_id_a.value + self.port_id_b.value
