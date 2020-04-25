from config_parser import *
from db_lib import *
from help_lib import initLogger
import json
import logging
import operator
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import subprocess
import time

# Since HardwareLibrary.py in diff folder, have to add to path before import
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../hardware-emulator/hardware_library')
from HardwareLibrary import HardwareLibrary

'''
TODO
integrate with hardware layer
master failover
    - If node that went down is also the master, initiate master failover:
        - if fail, move to next node?
    - assign extra static IP on aws, just for webapp. Whichever node hosts it
      claims the IP
'''

DATA_PUB_INTERVAL = 1
MASTER_WAIT_INTERVAL = 1

OPS = {"<"  : operator.lt,
       "<=" : operator.le,
       "==" : operator.eq,
       "!=" : operator.ne,
       ">=" : operator.ge,
       ">"  : operator.gt
}

# Make global so that handler functions can also access
conn = None
hardwareClient = None

# Should be called after you're certain that the ip address for the node marked
# as broker in the db is correct.
def initBrokerConnection():
    config = parseConfig()
    global conn

    # TODO: Error checking. what if broker not up? Then connect fails.
    # clean_session=True means every time we connect, delete old data.
    # client_id being something meaningful is useful for debugging, since broker
    # prints out info about clients based on the id
    if conn is not None:
        conn.loop_stop()
        print('reinitialising conn')
        conn = reinitialise()
        conn.reinitialise(client_id='node%d' % config['serial'],
                          clean_session=True)
    else:
        conn = mqtt.Client(client_id='node%d' % config['serial'],
                           clean_session=True)

    # Set a will. If node dies, broker will distribute payload.
    will = {'serial':config['serial']}
    conn.will_set(topic='heartbeats', payload=json.dumps(will), qos=2)

    conn.connect(getBrokerIp())

    # Subscribe to handle nodes' dying
    conn.message_callback_add('heartbeats', handleHeartbeats)
    conn.subscribe('heartbeats')

    # Start the async publishing loop. Manages sending mqtt network packets
    conn.loop_start()

    # Define disconnect behavior in case broker goes down
    conn.on_disconnect = handleDisconnect

    # Subscribe for status requests from the webapp
    topic = '%d/status_request' % config['serial']
    conn.message_callback_add(topic, handleStatusRequest)
    conn.subscribe(topic)

    # Subscribe for status change requests from the webapp
    topic = '%d/status_change_request' % config['serial']
    conn.message_callback_add(topic, handleStatusChangeRequest)
    conn.subscribe(topic)

    # Subscribe for updates from the webapp
    conn.message_callback_add('webapp/updates', handleWebappUpdate)
    conn.subscribe('webapp/updates')

    # Subscribe to all data streams for interactions if a device node
    if isDevice(config['serial']):
        for node in getAllNodes():
            if node['serial'] == config['serial']:
                continue

            topic = '%d/data_stream' % node['serial']
            conn.message_callback_add(topic, handleInteraction)
            conn.subscribe(topic)

# Used when webapps requests this node's status
def handleStatusRequest(client, userdata, message):
    # Ignore input, just send back the status.
    global conn, hardwareClient

    statusValue = hardwareClient.pollValue(getHardwareName())
    status = json.dumps({'status' : str(statusValue)})
    serial = parseConfig()['serial']
    conn.publish('%d/status_response' % serial, status)

def handleStatusChangeRequest(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))

    # Cast to correct type
    newVal = data['status']
    valType = getHardwareType()
    if valType == 'float':
        newVal = float(newVal)
    elif valType == 'boolean':
        newVal = bool(newVal)
    elif valType == 'integer':
        newVal = int(newVal)
    logging.info('Status change requested. New status: %s' % data['status'])

    global hardwareClient
    hardwareClient.changeValue(getHardwareName(), newVal)

def handleInteraction(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    sourceSerial = data['serial']

    # Don't make an actuation change if this node is not a device
    if not isDevice(parseConfig()['serial']):
        logging.info('node with serial %d triggered interaction, but is not device node'
                     % parseConfig()['serial'])
        return

    for i in getOwnInteractions():
        if i['trigger_serial'] == sourceSerial:
            operator = OPS[i['operator']]
            destVal = i['value']
            srcVal = data['data']

            if operator(srcVal, destVal):
                global hardwareClient

                # Cast to correct type
                newVal = i['action']
                valType = getHardwareType()
                if valType == 'float':
                    newVal = float(newVal)
                elif valType == 'boolean':
                    newVal = bool(newVal)
                elif valType == 'integer':
                    newVal = int(newVal)

                hardwareClient.changeValue(getHardwareName(), newVal)

                logging.info('interaction with id %d triggered' %
                             i['interaction_id'])

# TODO: need to actually manage the subscriptions subbed to... and the global
#       interactions dict
def handleWebappUpdate(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))

    if data['table'] == 'node_data':
        if data['type'] == 'update':
            updateNodeInDb(data['serial'], data['vals'])
            return

        logging.warning('Recieved update from webapp of incorrect type: '
                        + str(data))

    elif data['table'] == 'interactions':
        if data['type'] == 'add':
            writeInteractionToDb(data['vals'])

        elif data['type'] == 'delete':
            deleteInteractionFromDb(data['interaction_id'])

        elif data['type'] == 'update':
            deleteInteractionFromDb(data['interaction_id'])
            writeInteractionToDb(data['vals'])

        else:
            logging.warning('Recieved update from webapp of incorrect type: '
                            + str(data))
    else:
        logging.warning('Recieved update from webapp to incorrect table: '
                        + str(data))

def startMasterProc():
    logging.info('Starting master proc')
    print('Starting master proc')
    subprocess.call(['/bin/bash', '-c', './master.sh &'])
    # Give master time to start broker
    time.sleep(MASTER_WAIT_INTERVAL)

# This function deals with master failover, and returns the serial number of the
# new master to be promoted.
# Of the nodes that are currently up, returns the one with the lowest serial
def getNewMasterSerial():
    query = '''
        SELECT serial FROM node_data
        WHERE is_up = 1
        ORDER BY serial
    '''
    result = getSqlResult(query)
    if len(result) == 0:
        return parseConfig()['serial']

    return result[0][0]

# This function should assume that the master node has died, since the broker is
# dead, and should take care of master failover.
# @note: if in the future the broker is separated from the master node, this
#        will need to be changed.
def handleDisconnect(client, userdata, rc):
    logging.info('Broker has died with return code %d' % rc)
    oldMaster = getMasterSerial()

    # Make sure node is marked as dead
    setBoolCol(oldMaster, 'is_up', False)
    setBoolCol(oldMaster, 'last_up', int(time.time()))

    # Mark as not master and prepare for failover
    setBoolCol(oldMaster, 'is_master', False)
    setBoolCol(oldMaster, 'is_broker', False)

    newMaster = getNewMasterSerial()
    setBoolCol(newMaster, 'is_master', True)
    setBoolCol(newMaster, 'is_broker', True)

    if newMaster == parseConfig()['serial']:
        # Promote self
        logging.info('Promoting self to master')
        startMasterProc()

    # Connect to new master
    initBrokerConnection()


# A message will only publish to this topic if a node has disconnected
def handleHeartbeats(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    logging.info('node %d has died' % data['serial'])

    setBoolCol(data['serial'], 'is_up', False)
    setBoolCol(data['serial'], 'last_up', int(time.time()))

    # Could do 'if isMaster(data['serial']): doMasterFailover()'
    # However, if broker really died, then handleDisconnect will be triggered to
    # take care of the failover.

def main():
    initLogger()
    config = parseConfig()

    # TODO: uncomment this for production. I don't want random webapps rn.
    if isMaster(config['serial']):
       startMasterProc()

    global conn, hardwareClient

    # Init connection to hardware library
    hardwareDescription = parseHardwareDescription()
    hardwareClient = HardwareLibrary(hardwareDescription, 'http://3.21.193.233/emulator/')

    # Init broker connection
    initBrokerConnection()

    # Publish sensor data for other device's interactions
    topic = '%d/data_stream' % config['serial']
    while True:
        if isSensor(config['serial']):
            # TODO: this should eventually be generalized / propagated through the
            #       code to support multiple hardwares per node.
            data = {'data' : hardwareClient.pollValue(getHardwareName()),
                    'serial' : config['serial']}
            conn.publish(topic, json.dumps(data))

        time.sleep(DATA_PUB_INTERVAL)

if __name__ == '__main__':
    main()

