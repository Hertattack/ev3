from . import ValueMapping, MessageType, CommonMessageHeader


class ActionType(ValueMapping):
    SWITCH_OFF = b'\x01'
    DISCONNECT = b'\x02'
    VCC_PORT_CTRL_ON = b'\x03'
    VCC_PORT_CTRL_OFF = b'\x03'
    ACTIVATE_BUSY_INDICATION = b'\x05'
    RESET_BUSY_INDICATION = b'\x06'

    ACTION_RESPONSE_SWITCH_OFF = b'\x30'
    ACTION_RESPONSE_DISCONNECT = b'\x31'
    ACTION_RESPONSE_BOOT_MODE = b'\x32'


class ActionMessage:
    def __init__(self, action_type: bytes):
        self.action_type = ActionType(action_type)

    @property
    def value(self):
        header = CommonMessageHeader(1, MessageType.HUB_ACTION)
        return header.value + self.action_type.value
    