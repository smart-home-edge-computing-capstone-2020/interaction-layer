The interaction layer consists of the following programs:
Master
Node
Broker

Note that the master and node require the existence of a CONFIG file of the
following format:
{
    serial: unsigned integer, unique
    sensor: boolean, whether node produces sensing data
    device: boolean, whether node actuates physical changes (e.g. light on/off)
}

Since the serial number must be unique, this file is not committed, and must be
manually created on each new node.
