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

Some structure has been taken to make it simpler to implement and work with the library. Where relevant these are explained in this section.

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

### Messages

