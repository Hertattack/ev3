from src.poweredup.protocol import ProtocolError


class PortModeMapping:

    @classmethod
    def parse_bytes(cls, message_bytes):
        if len(message_bytes) > 1:
            raise ProtocolError("Expected a single byte for the port mode mapping")

        value = message_bytes[0]
        null_value_mapping = value & 128 == 128
        functional_mapping_2 = value & 64 == 64
        absolute_mapping = value & 16 == 16
        relative_mapping = value & 8 == 8
        discrete_mapping = value & 4 == 4

        return PortModeMapping(null_value_mapping, functional_mapping_2,
                               absolute_mapping, relative_mapping, discrete_mapping)

    def __init__(self, null_value, functional_mapping_2, absolute, relative, discrete):
        self.null_value = null_value
        self.functional_mapping_2 = functional_mapping_2
        self.absolute = absolute
        self.relative = relative
        self.discrete = discrete

    @property
    def value(self):
        value = (128 if self.null_value else 0) + \
                ( 64 if self.functional_mapping_2 else 0) + \
                ( 16 if self.absolute else 0) + \
                (  8 if self.relative else 0) + \
                (  4 if self.discrete else 0)

        return value.to_bytes(1, byteorder="big")
