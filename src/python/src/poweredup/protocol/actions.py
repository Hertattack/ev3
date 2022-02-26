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
    MAPPING = {
        b'\x01' : "SWITCH_OFF",
        b'\x02' : "DISCONNECT",
        b'\x03' : "VCC_PORT_CTRL_ON",
        b'\x03' : "VCC_PORT_CTRL_OFF",
        b'\x05' : "ACTIVATE_BUSY_INDICATION",
        b'\x06' : "RESET_BUSY_INDICATION",

        b'\x30' : "ACTION_RESPONSE_SWITCH_OFF",
        b'\x31' : "ACTION_RESPONSE_DISCONNECT",
        b'\x32' : "ACTION_RESPONSE_BOOT_MODE"
    }

    def __init__(self, message: bytes):
        pass