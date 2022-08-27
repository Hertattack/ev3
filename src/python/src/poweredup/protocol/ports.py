from . import ValueMapping, ProtocolError
from .messages import Message, CommonMessageHeader, MessageType


class PortID:
    def __init__(self, id_input):
        id_type = type(id_input)

        id_value = None
        if id_type == bytes:
            id_value = int.from_bytes(id_input, byteorder="big", signed=False)
        if id_type == int:
            id_value = id_input

        if id_value is None:
            raise ProtocolError(f"Unsupported id type supplied is not supported: {id_type}")

        if 0 > id_value > 255:
            raise ProtocolError(f"Expected id value between 0 and 255, but was {id_value}")

        self.value = id_value.to_bytes(1, byteorder="big", signed=False)
        self.id = id_value


class NotificationEnabledType(ValueMapping):
    DISABLED = b'\x00'
    ENABLED = b'\x01'


class InformationType(ValueMapping):
    PORT_VALUE = b'\x00'
    MODE_INFO = b'\x01'
    POSSIBLE_MODE_COMBINATIONS = b'\x02'


class ModeInformationType(ValueMapping):
    NAME = b'\x00'
    RAW = b'\x01'
    PERCENTAGE = b'\x02'
    SI = b'\x03'
    SYMBOL = b'\x04'
    MAPPING = b'\x05'
    INTERNAL_USE = b'\x06'
    MOTOR_BIAS = b'\x07'
    CAPABILITY_BITS = b'\x08'
    VALUE_FORMAT = b'\x80'


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


class PortModes:
    MODE_0 = 1
    MODE_1 = 2
    MODE_2 = 4
    MODE_3 = 8
    MODE_4 = 16
    MODE_5 = 32
    MODE_6 = 64
    MODE_7 = 128
    MODE_8 = 256
    MODE_9 = 512
    MODE_10 = 1024
    MODE_11 = 2048
    MODE_12 = 4096
    MODE_13 = 8192
    MODE_14 = 16384
    MODE_15 = 32768

    END_OF_COMBINATIONS = 0

    def __init__(self, mode_value: bytes):
        if len(mode_value) > 2:
            raise ProtocolError(f"Port mode cannot be longer than 2 bytes.")

        mode_int_value = int.from_bytes(mode_value, byteorder="big", signed=False)
        self.mode_0 = mode_int_value & PortModes.MODE_0 == PortModes.MODE_0
        self.mode_1 = mode_int_value & PortModes.MODE_1 == PortModes.MODE_1
        self.mode_2 = mode_int_value & PortModes.MODE_2 == PortModes.MODE_2
        self.mode_3 = mode_int_value & PortModes.MODE_3 == PortModes.MODE_3
        self.mode_4 = mode_int_value & PortModes.MODE_4 == PortModes.MODE_4
        self.mode_5 = mode_int_value & PortModes.MODE_5 == PortModes.MODE_5
        self.mode_6 = mode_int_value & PortModes.MODE_6 == PortModes.MODE_6
        self.mode_7 = mode_int_value & PortModes.MODE_7 == PortModes.MODE_7
        self.mode_8 = mode_int_value & PortModes.MODE_8 == PortModes.MODE_8
        self.mode_9 = mode_int_value & PortModes.MODE_9 == PortModes.MODE_9
        self.mode_10 = mode_int_value & PortModes.MODE_10 == PortModes.MODE_10
        self.mode_11 = mode_int_value & PortModes.MODE_11 == PortModes.MODE_11
        self.mode_12 = mode_int_value & PortModes.MODE_12 == PortModes.MODE_12
        self.mode_13 = mode_int_value & PortModes.MODE_13 == PortModes.MODE_13
        self.mode_14 = mode_int_value & PortModes.MODE_14 == PortModes.MODE_14
        self.mode_15 = mode_int_value & PortModes.MODE_15 == PortModes.MODE_15

    @property
    def value(self):
        return int.to_bytes( \
            (PortModes.MODE_0 if self.mode_0 else 0) + \
            (PortModes.MODE_1 if self.mode_1 else 0) + \
            (PortModes.MODE_2 if self.mode_2 else 0) + \
            (PortModes.MODE_3 if self.mode_3 else 0) + \
            (PortModes.MODE_4 if self.mode_4 else 0) + \
            (PortModes.MODE_5 if self.mode_5 else 0) + \
            (PortModes.MODE_6 if self.mode_6 else 0) + \
            (PortModes.MODE_7 if self.mode_7 else 0) + \
            (PortModes.MODE_8 if self.mode_8 else 0) + \
            (PortModes.MODE_9 if self.mode_9 else 0) + \
            (PortModes.MODE_10 if self.mode_10 else 0) + \
            (PortModes.MODE_11 if self.mode_11 else 0) + \
            (PortModes.MODE_12 if self.mode_12 else 0) + \
            (PortModes.MODE_13 if self.mode_13 else 0) + \
            (PortModes.MODE_14 if self.mode_14 else 0) + \
            (PortModes.MODE_15 if self.mode_15 else 0), \
            2, byteorder="big", signed=False)


class PortModeCombinationIndex(ValueMapping):
    INDEX_0 = b'\x01'
    INDEX_1 = b'\x02'
    INDEX_2 = b'\x03'
    INDEX_3 = b'\x04'
    INDEX_4 = b'\x05'
    INDEX_5 = b'\x06'
    INDEX_6 = b'\x07'
    INDEX_7 = b'\x08'


class PortModeInformationType(ValueMapping):
    NAME = b'\x00'
    RAW = b'\x01'
    PERCENTAGE = b'\x02'
    SI = b'\x03'
    SYMBOL = b'\x04'
    MAPPING = b'\x05'
    INTERNAL = b'\x06'
    MOTOR_BIAS_PCT = b'\x07'
    CAPABILITIES = b'\x08'
    VALUE_FORMAT = b'\x80'


class Capabilities:
    OUTPUT_FROM_HUB = 1
    INPUT_FROM_HUB = 2
    LOGICAL_COMBINABLE = 4
    LOGICAL_SYNCABLE = 8

    def __init__(self, mask: bytes):
        if len(mask) > 1:
            raise ProtocolError("Unsupported number of capability bytes.")

        mask_int_value = int.from_bytes(mask, byteorder="big")

        if mask_int_value > 15:
            raise ProtocolError(f"Unsupported bit-mask for capabilities {bin(ord(mask))}")

        self.is_output = mask_int_value & Capabilities.OUTPUT_FROM_HUB == Capabilities.OUTPUT_FROM_HUB
        self.is_input = mask_int_value & Capabilities.INPUT_FROM_HUB == Capabilities.INPUT_FROM_HUB
        self.is_combinable = mask_int_value & Capabilities.LOGICAL_COMBINABLE == Capabilities.LOGICAL_COMBINABLE
        self.is_syncable = mask_int_value & Capabilities.LOGICAL_SYNCABLE == Capabilities.LOGICAL_SYNCABLE

    @property
    def value(self):
        return int.to_bytes( \
            (Capabilities.OUTPUT_FROM_HUB if self.is_output else 0) + \
            (Capabilities.INPUT_FROM_HUB if self.is_input else 0) + \
            (Capabilities.LOGICAL_COMBINABLE if self.is_combinable else 0) + \
            (Capabilities.LOGICAL_SYNCABLE if self.is_syncable else 0), \
            1, byteorder="big", signed=False)


class PortInformationRequestMessage(Message):
    MESSAGE_TYPE = MessageType.PORT_INFO_REQ

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 2:
            raise ProtocolError(f"Message length different from expected length (2) = {message_length}")

        return PortInformationRequestMessage(PortID(message_bytes[0:1]), InformationType(message_bytes[1:]))

    def __init__(self, port_id: PortID, information_type: InformationType):
        self.port_id = port_id
        self.information_type = information_type

    @property
    def value(self):
        header = CommonMessageHeader(2, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.information_type.value


class PortModeInformationRequestMessage(Message):
    MESSAGE_TYPE = MessageType.PORT_MODE_INFO_REQ

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length != 3:
            raise ProtocolError("Message too long")

        portId = PortID(message_bytes[0:1])
        modeInformation = ModeInformationType(message_bytes[2:])
        return PortModeInformationRequestMessage(portId, message_bytes[1:2], modeInformation)

    def __init__(self, port_id: PortID, mode: bytes, mode_information: ModeInformationType):
        self.port_id = port_id
        self.mode = mode
        self.mode_information = mode_information

    @property
    def value(self):
        header = CommonMessageHeader(3, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + self.mode + self.mode_information.value


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


class PortInformation(Message):
    MESSAGE_TYPE = MessageType.PORT_INFO

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)

        if message_length < 4:
            raise ProtocolError("At least 4 bytes of payload expected.")

        port_id = PortID(message_bytes[0:1])
        information_type = InformationType(message_bytes[1:2])

        if information_type != InformationType.MODE_INFO \
                and information_type != InformationType.POSSIBLE_MODE_COMBINATIONS:
            raise ProtocolError(f"Unsupported information type for this message type: {information_type.name}")

        if information_type == InformationType.MODE_INFO:
            if message_length != 8:
                raise ProtocolError(
                    f"Expected length of 8 bytes for message payload for information type: {information_type.name}.")

            capabilities = Capabilities(message_bytes[2:3])
            total_count_mode = int.from_bytes(message_bytes[3:4], byteorder="big", signed=False)
            input_modes = PortModes(message_bytes[4:6])
            output_modes = PortModes(message_bytes[6:])

            return PortInformation(port_id, information_type,
                                   capabilities=capabilities, total_count_mode=total_count_mode,
                                   input_modes=input_modes, output_modes=output_modes)

        mode_combinations = []
        mode_index = 2
        while mode_index < message_length:
            mode_combinations.append(PortModes(message_bytes[mode_index:mode_index + 2]))
            mode_index = mode_index + 2

        return PortInformation(port_id, information_type, mode_combinations=mode_combinations)

    def __init__(self, port_id: PortID, information_type: InformationType,
                 capabilities: Capabilities = None, total_count_mode: int = None,
                 input_modes: PortModes = None, output_modes: PortModes = None,
                 mode_combinations: list[int] = None):

        if information_type == InformationType.MODE_INFO and mode_combinations is not None:
            raise ProtocolError("Mode combinations not supported for information type mode info.")

        if information_type == InformationType.MODE_INFO and (capabilities is None or total_count_mode is None or
                                                              input_modes is None or output_modes is None):
            raise ProtocolError(
                "For mode info, capabilities, total count mode, input and output modes need to be given")

        if information_type == InformationType.POSSIBLE_MODE_COMBINATIONS and (capabilities is not None or
                                                                               total_count_mode is not None or
                                                                               input_modes is not None or
                                                                               output_modes is not None):
            raise ProtocolError("For possible mode combinations, only mode combinations can be given")

        if information_type == InformationType.POSSIBLE_MODE_COMBINATIONS and mode_combinations is None:
            raise ProtocolError("For possible mode combinations, mode combinations needs to be specified.")

        self.port_id = port_id
        self.information_type = information_type
        self.capabilities = capabilities
        self.total_count_mode = total_count_mode
        self.input_modes = input_modes
        self.output_modes = output_modes
        self.mode_combinations = mode_combinations

    @property
    def value(self):
        if self.information_type == InformationType.MODE_INFO:
            header = CommonMessageHeader(8, self.MESSAGE_TYPE)
            return header.value + self.port_id.value + self.information_type.value + self.capabilities.value + \
                self.total_count_mode.to_bytes(1, byteorder="big", signed=False) + \
                self.input_modes.value + self.output_modes.value
        else:
            combinations = len(self.mode_combinations)
            header = CommonMessageHeader(2 + combinations * 2, self.MESSAGE_TYPE)
            message_bytes = self.mode_combinations[0].value
            combination_index = 1
            while combination_index < combinations:
                message_bytes = message_bytes + self.mode_combinations[combination_index].value
                combination_index = combination_index + 1
            return header.value + self.port_id.value + self.information_type.value + message_bytes


class PortModeInformation(Message):
    MESSAGE_TYPE = MessageType.PORT_MODE_INFO

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        message_length = len(message_bytes)
        if message_length < 4:
            raise ProtocolError("Expected length of at least 4 bytes for message payload.")

        port_id = PortID(message_bytes[0:1])
        information_format = PortModeInformationFormat.parse_bytes(message_bytes[1:])

        return PortModeInformation(port_id, information_format)

    def __init__(self, port_id, information_format):
        self.port_id = port_id
        self.mode_information_type = information_format.MODE_INFORMATION_TYPE
        self.mode_information = information_format

    @property
    def value(self):
        mode_information_bytes = self.mode_information.value
        header = CommonMessageHeader(len(mode_information_bytes)+1, self.MESSAGE_TYPE)
        return header.value + self.port_id.value + mode_information_bytes


class PortModeInformationFormat:

    @classmethod
    def parse_bytes(cls, message_bytes: bytes):
        mode = message_bytes[0:1]
        mode_information_type = PortModeInformationType(message_bytes[1:2])
        match mode_information_type.value:
            case PortModeInformationName.MODE_INFORMATION_TYPE.value:
                return PortModeInformationName.parse_bytes(mode, message_bytes[2:])
            case PortModeInformationRaw.MODE_INFORMATION_TYPE.value:
                return PortModeInformationRaw.parse_bytes(mode, message_bytes[2:])
            case PortModeInformationPercentage.MODE_INFORMATION_TYPE.value:
                return PortModeInformationPercentage.parse_bytes(mode, message_bytes[2:])
            case PortModeInformationSi.MODE_INFORMATION_TYPE.value:
                return PortModeInformationSi.parse_bytes(mode, message_bytes[2:])

        raise ProtocolError(f"Unimplemented port mode information type encountered: '{mode_information_type.name}'")

    @classmethod
    def validate(cls, message_bytes: bytes, max_length: int = None, expected_length: int = None):
        message_length = len(message_bytes)
        if expected_length and message_length != expected_length:
            message = 'Message length: {length} is different from expected length: {expected}. For type: {typename}' \
                .format(length=message_length, expected=expected_length, typename=cls.MODE_INFORMATION_TYPE.name)
            raise ProtocolError(message)
        if max_length and message_length > max_length:
            message = 'Message length: {length} is larger than allowed length of: {expected}. For type: {typename}' \
                .format(length=message_length, expected=max_length, typename=cls.MODE_INFORMATION_TYPE.name)
            raise ProtocolError(message)

    def __init__(self, mode):
        self.mode = mode

    @property
    def value(self):
        return self.mode + self.MODE_INFORMATION_TYPE.value


class PortModeInformationName(PortModeInformationFormat):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.NAME)

    MAX_LENGTH = 11

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, max_length=PortModeInformationName.MAX_LENGTH)

        name = ""

        for char_int_value in message_bytes:
            if not ((48 <= char_int_value <= 57) or (65 <= char_int_value <= 90) or (
                    97 <= char_int_value <= 122) or char_int_value == 95):
                raise ProtocolError(f"Name contains unsupported characters: {chr(char_int_value)}")

            name += chr(char_int_value)

        return PortModeInformationName(mode, name)

    def __init__(self, mode, name):
        super().__init__(mode)
        self.name = name

    @property
    def value(self):
        return super().value + bytes(self.name, 'UTF-8')


class PortModeInformationFloatingPointValues(PortModeInformationFormat):
    MAX_LENGTH = 8

    @classmethod
    def parse_bytes(cls, mode: bytes, message_bytes: bytes):
        cls.validate(message_bytes, max_length=PortModeInformationName.MAX_LENGTH)

        return cls(mode, message_bytes)

    def __init__(self, mode, byte_value):
        super().__init__(mode)
        self.byte_value = byte_value

    @property
    def value(self):
        return super().value + self.byte_value


class PortModeInformationRaw(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.RAW)


class PortModeInformationPercentage(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.PERCENTAGE)


class PortModeInformationSi(PortModeInformationFloatingPointValues):
    MODE_INFORMATION_TYPE = ModeInformationType(ModeInformationType.SI)
