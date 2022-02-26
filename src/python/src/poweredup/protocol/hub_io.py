from . import ValueMapping, VersionNumberEncoding
from .messages import MessageType, CommonMessageHeader
from ports import PortID


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


class AttachedIoMessage:

    def __init__(self, port_id, event_type: bytes,
                 attached_io_type=None,
                 hw_revision=None, sw_revision=None,
                 port_a_id=None, port_b_id=None):
        if event_type == EventType.DETACHED_IO and (
                        attached_io_type is not None or
                        hw_revision is not None or sw_revision is not None or
                        port_a_id is not None or port_b_id is not None):
            raise "Unsupported arguments for detached IO."

        if event_type != EventType.DETACHED_IO and attached_io_type is None:
            raise "Expected attached io type to be specified."

        if event_type == EventType.ATTACHED_IO and (port_a_id is not None or port_b_id is not None):
            raise "Port a and b can only be specified for virtual events."

        if event_type == EventType.ATTACHED_IO and (hw_revision is None or sw_revision is None):
            raise "Expected hw and sw revision to be specified for attached io."

        if event_type == EventType.VIRTUAL_IO and (hw_revision is not None or sw_revision is not None):
            raise "Expected hw and sw revision to be none for virtual io."

        if event_type == EventType.VIRTUAL_IO and (port_a_id is None or port_b_id is None):
            raise "Expected port a and b to be set for virtual io."

        self.port_id = PortID(port_id)
        self.event_type = EventType(event_type)

        self.attached_io_type = None if attached_io_type is None else IOType(attached_io_type)

        self.hw_revision = None if hw_revision is None else VersionNumberEncoding(hw_revision)
        self.sw_revision = None if sw_revision is None else VersionNumberEncoding(sw_revision)

        self.port_id_a = None if port_a_id is None else PortID(port_a_id)
        self.port_id_b = None if port_b_id is None else PortID(port_b_id)
