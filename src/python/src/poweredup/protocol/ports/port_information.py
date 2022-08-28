from src.poweredup.protocol import ProtocolError, ValueMapping
from src.poweredup.protocol.messages import Message, MessageType, CommonMessageHeader
from src.poweredup.protocol.ports.port import PortID, PortModes, Capabilities


class InformationType(ValueMapping):
    PORT_VALUE = b'\x00'
    MODE_INFO = b'\x01'
    POSSIBLE_MODE_COMBINATIONS = b'\x02'


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

