from db_lib import writeNodeToDb, writeInteractionToDb
import time

# Nodes
n1 = {
        'serial' : 1,
        'ip_address' : '34.233.41.49',
        'is_master' : True,
        'is_broker' : True,
        'is_device' : True,
        'is_sensor' : True,
        'is_up' : True,
        'last_up' : int(time.time()),
        'display_name' : 'Node 1',
        'description' : 'Da first of da nodes'
}

n2 = {
        'serial' : 2,
        'ip_address' : '18.208.23.252',
        'is_master' : False,
        'is_broker' : False,
        'is_device' : True,
        'is_sensor' : True,
        'is_up' : True,
        'last_up' : int(time.time()),
        'display_name' : 'Node 2',
        'description' : 'Da second of da nodes'
}

n3 = {
        'serial' : 3,
        'ip_address' : '3.213.43.206',
        'is_master' : False,
        'is_broker' : False,
        'is_device' : True,
        'is_sensor' : True,
        'is_up' : True,
        'last_up' : int(time.time()),
        'display_name' : 'Node 3',
        'description' : 'Da third of da nodes'
}

writeNodeToDb(n1)
writeNodeToDb(n2)
writeNodeToDb(n3)

# Interactions

i1 = {
        'trigger_serial' : 2,
        'operator' : '<',
        'value' : 5,
        'target_serial' : 1,
        'action' : 15213.0,
        'display_name' : 'Interaction 2',
        'description' : 'Da first of da interactions'
}

i2 = {
        'trigger_serial' : 2,
        'operator' : '<',
        'value' : 1,
        'target_serial' : 1,
        'action' : -1234.0,
        'display_name' : 'Interaction 1',
        'description' : 'Da second of da interactions'
}

writeInteractionToDb(i1)
writeInteractionToDb(i2)
