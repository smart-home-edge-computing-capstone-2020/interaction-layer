from db_lib import writeNodeToDb
import time

# This file is meant to facilitiate loading the db with the initial node data
node1 = {
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

node2 = {
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

node3 = {
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

writeNodeToDb(node1)
writeNodeToDb(node2)
writeNodeToDb(node3)
