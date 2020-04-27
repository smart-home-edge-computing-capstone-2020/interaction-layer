This directory includes the following files:
- trigger.txt: a list of published messages with timestamps and message ids
- target.txt: matching messages recieved by another node in the system, and the
  time at which it acted upon the interaction.
- avg\_interaction\_delay.py: a script that takes the difference between
  matching messages and averages all the differences.

The data in this folder was collected by running 5 nodes, of which there were
2 sensor nodes, 2 device nodes, and one combined sensor / device node. There
were 6 interactions defined and running, although the logs here are for
1 interaction in particular (a random of the 6).

Based on this data, the average delay between a sensor node publishing data and
a device node reacting based off of a saved interaction is
__0.00276 seconds__.

Additional information: the nodes used in particular were defined as follows:
```
node1 = {
        'serial' : 1,
        'is_master' : True,
        'is_device' : False,
        'is_sensor' : True,
        'display_name' : 'Proximity Sensor 1',
}

node2 = {
        'serial' : 2,
        'is_master' : False,
        'is_device' : False,
        'is_sensor' : True,
        'display_name' : 'Proximity Sensor 2',
}

node3 = {
        'serial' : 3,
        'is_master' : False,
        'is_device' : True,
        'is_sensor' : True,
        'display_name' : 'Alarm Clock',
}

node4 = {
        'serial' : 4,
        'is_master' : False,
        'is_device' : True,
        'is_sensor' : False,
        'display_name' : 'Coffee Pot',
}

node5 = {
        'serial' : 5,
        'is_master' : False,
        'is_device' : True,
        'is_sensor' : False,
        'display_name' : 'LED Lamp',
}
```
