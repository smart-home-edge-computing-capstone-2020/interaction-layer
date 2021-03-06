from db_lib import writeNodeToDb, writeInteractionToDb
import time

# This file is meant to facilitiate loading the db with the initial node data
node1 = {
    'serial' : 1,
    'ip_address' : '34.233.41.49',
    'is_master' : True,
    'is_broker' : True,
    'is_device' : False,
    'is_sensor' : True,
    'is_up' : True,
    'last_up' : int(time.time()),
    'display_name' : 'Bedroom Proximity Sensor',
    'description' : 'Motion detector'
}

node2 = {
    'serial' : 2,
    'ip_address' : '18.208.23.252',
    'is_master' : False,
    'is_broker' : False,
    'is_device' : False,
    'is_sensor' : True,
    'is_up' : True,
    'last_up' : int(time.time()),
    'display_name' : 'Kitchen Proximity Sensor',
    'description' : 'Motion detector'
}

node3 = {
    'serial' : 3,
    'ip_address' : '3.213.43.206',
    'is_master' : False,
    'is_broker' : False,
    'is_device' : True,
    'is_sensor' : True,
    'is_up' : True,
    'last_up' : int(time.time()),
    'display_name' : 'Alarm Clock',
    'description' : 'Wakes me up in the morning'
}

node4 = {
    'serial' : 4,
    'ip_address' : '18.210.201.94',
    'is_master' : False,
    'is_broker' : False,
    'is_device' : True,
    'is_sensor' : False,
    'is_up' : True,
    'last_up' : int(time.time()),
    'display_name' : 'Coffee Pot',
    'description' : 'This coffee was so expensive but it helps wake me up'
}

node5 = {
    'serial' : 5,
    'ip_address' : '50.16.106.15',
    'is_master' : False,
    'is_broker' : False,
    'is_device' : True,
    'is_sensor' : False,
    'is_up' : True,
    'last_up' : int(time.time()),
    'display_name' : 'Bedroom Light',
    'description' : 'Makes my life more lit'
}

writeNodeToDb(node1)
writeNodeToDb(node2)
writeNodeToDb(node3)
writeNodeToDb(node4)
writeNodeToDb(node5)



interaction1 = {
    'trigger_serial' : 3,
    'target_serial' : 4,
    'operator' : '>',
    'value' : 0,
    'action' : 1,
    'display_name' : 'Make me coffee',
    'description' : 'When my alarm goes off, start brewing my coffee',
}

interaction2 = {
    'trigger_serial' : 1,
    'target_serial' : 5,
    'operator' : '>',
    'value' : 0,
    'action' : 1,
    'display_name' : 'Turn my lights on',
    'description' : 'When I get out of bed, turn my lights on',
}

interaction3 = {
    'trigger_serial' : 1,
    'target_serial' : 5,
    'operator' : '<',
    'value' : 1,
    'action' : 0,
    'display_name' : 'Turn my lights off',
    'description' : 'When I leave my bedroom, turn off the lights',
}

writeInteractionToDb(interaction1)
writeInteractionToDb(interaction2)
writeInteractionToDb(interaction3)
