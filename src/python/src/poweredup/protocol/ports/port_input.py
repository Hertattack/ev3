from src.poweredup.protocol import ProtocolError, ValueMapping
from src.poweredup.protocol.messages import Message, MessageType, CommonMessageHeader
from src.poweredup.protocol.ports.port import PortID
from src.poweredup.protocol.ports.port_mode_information import PortModeCombinationIndex


class NotificationEnabledType(ValueMapping):
    DISABLED = b'\x00'
    ENABLED = b'\x01'


class SubCommandType(ValueMapping):
    SET_MODE_AND_DATASET = b'\x01'
    LOCK_LPF2_DEV_SETUP = b'\x02'
    UNLOCK_MULTI_UPDATE_ENABLED = b'\x03'
    UNLOCK_MULTI_UPDATE_DISABLED = b'\x04'
    UNUSED = b'\x05'
    RESET_SENSOR_TO_LEGACY_MODE = b'\x06'


class DataSetFormatType(ValueMapping):
    DATA_8BIT_SIGNED_INT = b'\x01'
    DATA_16BIT_SIGNED_LE_INT = b'\x02'
    DATA_32BIT_SIGNED_LE_INT = b'\x03'
    DATA_FLOAT = b'\x04'


class PortInputFormatSetupSingle(Message):
    MESSAGE_TYPE = MessageType.PORT_INPUT_FORMAT_SETUP_SINGLE

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 7:
            raise ProtocolError("Expected length of 6 bytes for message payload.")

        port_id = PortID(message_bytes[0:1])
        mode = message_bytes[1:2]
        delta_interval = message_bytes[2:6]
        notification_enabled = NotificationEnabledType(message_bytes[7:])

        return PortInputFormatSetupSingle(port_id, mode, delta_interval, notification_enabled)

    def __init__(self, port_id: PortID, mode: bytes, delta_interval: bytes,
                 notification_enabled: NotificationEnabledType):
        if len(mode) != 1:
            raise ProtocolError("Expected length of mode is 1 bytes.")

        if len(delta_interval) != 4:
            raise ProtocolError("Expected length of delta interval is 4 bytes (uint32)")

        self.port_id = port_id
        self.mode = mode
        self.delta_interval = delta_interval
        self.notification_enabled = notification_enabled

    @property
    def value(self):
        header = CommonMessageHeader(7, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.mode + self.delta_interval + \
               self.notification_enabled.value


class PortInputFormatSetupCombined(Message):
    MESSAGE_TYPE = MessageType.PORT_INPUT_FORMAT_SETUP_COMBINED

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length < 2:
            raise ProtocolError("Expected message length of at least 2 bytes")

        port_id = PortID(message_bytes[0:1])
        sub_command = SubCommandType(message_bytes[1:2])

        if sub_command == SubCommandType.SET_MODE_AND_DATASET and message_length != 4:
            raise ProtocolError(f"Expected message length of exactly 4 bytes for sub command: {sub_command.name}")

        if sub_command != SubCommandType.SET_MODE_AND_DATASET and message_length != 2:
            raise ProtocolError(f"Expected message length of exactly 2 bytes for sub command: {sub_command.name}")

        if sub_command != SubCommandType.SET_MODE_AND_DATASET:
            return PortInputFormatSetupCombined(port_id, sub_command)

        combination_index = PortModeCombinationIndex(message_bytes[2:3])

        return PortInputFormatSetupCombined(port_id, sub_command, combination_index, message_bytes[3:])

    def __init__(self, port_id: PortID, sub_command: SubCommandType,
                 combination_index: PortModeCombinationIndex = None, mode_dataset: bytes = None):

        if sub_command == SubCommandType.SET_MODE_AND_DATASET:
            if combination_index is None or mode_dataset is None:
                raise ProtocolError("For setting mode and data set, combination index and mode data set value needed.")
        elif combination_index is not None or mode_dataset is not None:
            raise ProtocolError("For other sub commands than setting mode and data set, combination index and mode "
                                "and data set value are not allowed.")

        self.port_id = port_id
        self.sub_command = sub_command
        self.combination_index = combination_index
        self.mode_dataset = mode_dataset

    @property
    def value(self):
        length = 2 if self.sub_command != SubCommandType.SET_MODE_AND_DATASET else 4
        header = CommonMessageHeader(length, self.MESSAGE_TYPE)
        value = header + self.port_id.value + self.sub_command.value
        if self.sub_command == SubCommandType.SET_MODE_AND_DATASET:
            value = value + self.combination_index.value + self.mode_dataset
        return value

