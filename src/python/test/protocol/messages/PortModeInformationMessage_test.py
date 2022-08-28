import struct

from src.poweredup.protocol import ProtocolError
from src.poweredup.protocol.messages import Message
import src.poweredup.protocol.handling


def test_port_mode_information_name_message_is_supported():
    # header, port id, mode, type, name
    message_bytes = b'\x0b\x00\x44\x01\x00\x00\x48\x45\x4C\x4C\x4F'
    message = Message.parse_bytes(message_bytes)
    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "NAME"
    assert message.mode_information.name == "HELLO"


def test_port_mode_information_name_message_validates_length():
    # header, port id, mode, type, name
    message_bytes = b'\x09\x00\x44\x01\x00\x00\x48\x45\x4C\x4C\x4F\x48\x45\x4C\x4C\x4F\x48\x45\x4C\x4C\x4F'
    try:
        message = Message.parse_bytes(message_bytes)
        assert False
    except ProtocolError as protocolError:
        assert protocolError.message == "Message length: 15 is larger than allowed length of: 11. For type: NAME"


def test_port_mode_information_name_message_validates_allowed_characters():
    # header, port id, mode, type, name
    message_bytes = b'\x09\x00\x44\x01\x00\x00\x48\x45\x4C\x60\x4C\x4F'
    try:
        message = Message.parse_bytes(message_bytes)
        assert False
    except ProtocolError as protocolError:
        assert protocolError.message == 'Name contains unsupported characters: `'


def test_port_mode_information_raw_message_is_supported():
    min_value = struct.pack(">f", 2.0)
    max_value = struct.pack(">f", -6.5)

    message_bytes = b'\x0E\x00\x44\x01\x00\x01' + min_value + max_value
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "RAW"
    assert message.mode_information.min_value == float(2.0)
    assert message.mode_information.max_value == float(-6.5)


def test_port_mode_information_percentage_message_is_supported():
    min_value = struct.pack(">f", 5.0)
    max_value = struct.pack(">f", -4.5)

    message_bytes = b'\x0E\x00\x44\x01\x00\x02' + min_value + max_value
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "PERCENTAGE"
    assert message.mode_information.min_value == float(5.0)
    assert message.mode_information.max_value == float(-4.5)


def test_port_mode_information_si_message_is_supported():
    min_value = struct.pack(">f", -1)
    max_value = struct.pack(">f", 2)

    message_bytes = b'\x0E\x00\x44\x01\x00\x03' + min_value + max_value
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "SI"
    assert message.mode_information.min_value == float(-1)
    assert message.mode_information.max_value == float(2)


def test_port_mode_symbol_message_is_supported():
    message_bytes = b'\x09\x00\x44\x01\x00\x04\x44\x45\x47'
    message = Message.parse_bytes(message_bytes)
    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "SYMBOL"
    assert message.mode_information.symbol == "DEG"


def test_port_mode_mapping_message_is_supported():
    message_bytes = b'\x08\x00\x44\x01\x00\x05\x58\xCC'
    message = Message.parse_bytes(message_bytes)
    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "MAPPING"

    input_mapping = message.mode_information.input_mapping
    assert input_mapping.null_value == False
    assert input_mapping.functional_mapping_2 == True
    assert input_mapping.absolute == True
    assert input_mapping.relative == True
    assert input_mapping.discrete == False

    output_mapping = message.mode_information.output_mapping
    assert output_mapping.null_value == True
    assert output_mapping.functional_mapping_2 == True
    assert output_mapping.absolute == False
    assert output_mapping.relative == True
    assert output_mapping.discrete == True


def test_port_mode_motor_bias_message_is_supported():
    message_bytes = b'\x07\x00\x44\x01\x00\x07\x38'
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "MOTOR_BIAS"
    assert message.mode_information.bias == 56


def test_port_mode_motor_bias_message_guards_overflow():
    message_bytes = b'\x07\x00\x44\x01\x00\x07\x65'
    try:
        Message.parse_bytes(message_bytes)
        assert False
    except ProtocolError as error:
        assert error.message == "Motor bias value 101 out of range: 0 - 100"


def test_port_mode_sensor_capabilities_message_is_supported():
    message_bytes = b'\x0C\x00\x44\x01\x00\x08\x01\x02\x03\x04\x05\x06'
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "CAPABILITY_BITS"
    assert message.mode_information.capabilities.hex() == message_bytes[6:].hex()


def test_port_mode_sensor_capabilities_length_is_checked():
    message_bytes = b'\x0D\x00\x44\x01\x00\x08\x01\x02\x03\x04\x05\x06\x07'

    try:
        Message.parse_bytes(message_bytes)
        assert False
    except ProtocolError as error:
        assert error.message == "Message length: 7 is different from expected length: 6. For type: CAPABILITY_BITS"


def test_port_mode_value_message_is_supported():
    message_bytes = b'\x0A\x00\x44\x01\x00\x80\x07\x01\x13\x00'
    message = Message.parse_bytes(message_bytes)

    assert message.value.hex() == message_bytes.hex()
    assert message.mode_information_type.name == "VALUE_FORMAT"

    value_format = message.mode_information.value_format
    assert value_format.data_set_count == 7
    assert value_format.data_set_type.name == "SIXTEEN_BIT"
    assert value_format.nr_of_figures == 19
    assert value_format.nr_of_decimals == 0


def test_port_mode_value_length_is_checked():
    message_bytes = b'\x0A\x00\x44\x01\x00\x80\x07\x01\x13\x00\x12'

    try:
        Message.parse_bytes(message_bytes)
        assert False
    except ProtocolError as error:
        assert error.message == "Message length: 5 is different from expected length: 4. For type: VALUE_FORMAT"

