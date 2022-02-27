# Implementation of the LEGO BLE Wireless Protocol

[Protocol version: 3.0.0.0 (r17)](https://lego.github.io/lego-ble-wireless-protocol-docs/index.html)

In general the focus is on the part of the specification that will allow motor movement and clear feedback from the device.

The following parts will not be supported (message type):

* H/W Network Commands (0x08)
* Go Into Boot Mode (0x10)
* F/W Update Lock Memory (0x11)
* F/W Update Lock Status Request (0x12)
* F/W Update Lock Status (0x13)

**Current status:**

The specification is large and my time limited, that means that only a small portion is implemented currently. This has not been tested with tha actual device yet.

There are several unit-tests for the code to at least validate that the code works within my understanding of the specification.

## Patterns and Structure

Some structure has been added to make it simpler to implement and work with the library. Where relevant these are explained in this section.

In general, the focus is on exchanging messages. You need to be able to create messages easily and with limited knowledge of the underlying message format. To achieve this the messages as specified in are implemented as Python classes that should make it simpler to construct the right messages and understand the feedback from the device.

### Value Mappings

There are many fixed values that represent states, types and other information. These have been translated into a common structure that can be used.

An example is the AlertStatus, the definition looks as follows:

```python
from protocol import ValueMapping

class AlertStatus(ValueMapping):
    OK = b'\x00'
    ALERT = b'\xFF'
```

Using it is done like this:

```python
from protocol.alerts import AlertStatus

status = AlertStatus(AlertStatus.OK)
status == AlertStatus.OK
status.value == b'\x00' == AlertStatus.OK
status.name == "OK"

unsupported_value = b'\x42'
status = AlertStatus(unsupported_value) # will raise an error
```

Under the hood, the capitalized properties are taken and added to a mapping. If you create an instance with the value it will have the name of the property and the value by which it was recognized or an exception if the value could not be mapped.

### Messages

The messages are the foundation of the protocol library. They can either be created from a bytes value that is coming from the bluetooth communication or using a more human friendly way to make the protocol more accessible.

The generic pattern:

```python
from protocol import ProtocolError
from protocol.messages import Message, CommonMessageHeader

# you inherit from the Message class
class SomeMessage(Message):
    # the message class expects this attribute to be present to determine if an incoming
    # message can be parsed by this class.
    MESSAGE_TYPE = b'\x42'
    
    # and implement a class method to parse the payload into a message
    # this method is used by the Message class, so the name is important
    @classmethod
    def parse_bytes(cls, payload_bytes: bytes):
        # checks and conversions
        if len(payload_bytes) != 2:
            raise ProtocolError("Expected 2 bytes for the payload.")
        int_value = int.from_bytes(payload_bytes, byteorder="big", signed=True)
        return cls(int_value)
    
    # the constructor contains the "human" friendly way of creating the message
    def __init__(self, counter_value: int):
        if -10 < counter_value > 10:
            raise ProtocolError(f"Counter value should be between -10 and 10")
        
        self.counter_value = counter_value

    # to be able to send the message this is an example implementation
    # this name is used from the method class in the override of the equality operator
    @property
    def value(self):
        # note, use the length of the payload, not the length of the full message
        header = CommonMessageHeader(2, SomeMessage.MESSAGE_TYPE)
        return header.value + int.to_bytes(self.counter_value, 2, byteorder="big", signed=True)
```

Using the code:
```python
from protocol.messages import Message
from protocol.some import SomeMessage

# parsing bytes coming in, assume this is the full message:
message_bytes = b'\x05\x00\x42\x00\x05'
message: SomeMessage = Message.parse_bytes(message_bytes)
message.counter_value == 5
message.value == message_bytes

# creating a new message using the constructor
message: SomeMessage = SomeMessage(5)
message.counter_value == 5
message.value == b'\x05\x00\x42\x00\x05'
```