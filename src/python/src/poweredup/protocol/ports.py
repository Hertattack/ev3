from . import ValueMapping


class PortID:
    def __init__(self, id_input):
        id_type = type(id_input)

        id_value = None
        if id_type == bytes:
            id_value = int.from_bytes(id_input, byteorder="big", signed=False)
        if id_type == int:
            id_value = id_input

        if id_value is None:
            raise f"Unsupported id type supplied is not supported: {id_type}"

        if 0 > id_value > 255:
            raise f"Expected id value between 0 and 255, but was {id_value}"

        self.value = id_value.to_bytes(1, byteorder="big", signed=False)
        self.id = id_value