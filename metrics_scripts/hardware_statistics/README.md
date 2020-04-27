This directory includes the following files:
- cpu.txt: an analysis of the cpu usage of each node
- net\_in.txt: an analysis of the bytes into each node
- net\_out.txt: an analysis of the bytes out of each node
- disk\_usage.txt: an analysis of the disk usage used by the system
- graphs/: screenshot of aws cloudwatch graphs showing network and cpu usage of
  each node. Note that node1 is the master node in these graphs.

Note that the data here has to be taken with a grain of salt, as its statistic
on virtualized hardware. We don't have control over exactly when anything runs,
and it's possible that due to they hypervisor, certain statistics are skewed.
Another possible reason for the variety in the data is the way the interactions
were defined; it's possible that some nodes ended up having to do a little more
or less work.

The data in this folder was collected by running 5 nodes, of which there were
2 sensor nodes, 2 device nodes, and one combined sensor / device node. There
were 6 interactions defined and running.

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
