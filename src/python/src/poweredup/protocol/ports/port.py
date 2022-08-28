from src.poweredup.protocol import ProtocolError


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
        return int.to_bytes(
            (PortModes.MODE_0 if self.mode_0 else 0) +
            (PortModes.MODE_1 if self.mode_1 else 0) +
            (PortModes.MODE_2 if self.mode_2 else 0) +
            (PortModes.MODE_3 if self.mode_3 else 0) +
            (PortModes.MODE_4 if self.mode_4 else 0) +
            (PortModes.MODE_5 if self.mode_5 else 0) +
            (PortModes.MODE_6 if self.mode_6 else 0) +
            (PortModes.MODE_7 if self.mode_7 else 0) +
            (PortModes.MODE_8 if self.mode_8 else 0) +
            (PortModes.MODE_9 if self.mode_9 else 0) +
            (PortModes.MODE_10 if self.mode_10 else 0) +
            (PortModes.MODE_11 if self.mode_11 else 0) +
            (PortModes.MODE_12 if self.mode_12 else 0) +
            (PortModes.MODE_13 if self.mode_13 else 0) +
            (PortModes.MODE_14 if self.mode_14 else 0) +
            (PortModes.MODE_15 if self.mode_15 else 0),
            2, byteorder="big", signed=False)


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
        return int.to_bytes(
            (Capabilities.OUTPUT_FROM_HUB if self.is_output else 0) +
            (Capabilities.INPUT_FROM_HUB if self.is_input else 0) +
            (Capabilities.LOGICAL_COMBINABLE if self.is_combinable else 0) +
            (Capabilities.LOGICAL_SYNCABLE if self.is_syncable else 0),
            1, byteorder="big", signed=False)
