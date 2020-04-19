from config_parser import *
from db_lib import getOwnInteractions, getBrokerIp, isMaster
from db_lib import deleteInteractionFromDb, writeInteractionToDb
from db_lib import updateNodeInDb
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
interactions should be ironed out

heartbeats
master failover
    - look into nodes adding wills to a heartbeats topic, if they randomly
      disconnect it'll get sent to everyone.
    - define an on_disconnect for the client? so if broker goes down can promote
    - assign extra static IP on aws, just for webapp. Whichever node hosts it
      claims the IP

DONE
nodes should respond statuses
'config changes' from webapp
    add (interaction), provide all data
    delete (interaction), provide interaction id
    update (interaction): I just call the above 2 in order
    update (node), provide new description AND name (maybe optional and I search?)
'''

SLEEP_TIME = 1
interactions = dict()
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

# Used when webapps requests this node's status
def handleStatusRequest(client, userdata, message):
    # Ignore input, just send back the status.
    global conn
    # TODO: add Rips status here
    status = json.dumps({'status' : 'on'})
    serial = parseConfig()['serial']
    conn.publish('%d/status_response' % serial, status)

def handleInteraction(client, userdata, message):
    # TODO: maybe pull this from the message?
    sourceSerial = int(message.topic.split('/')[0])
    data = json.loads(message.payload.decode('utf-8'))

    for i in interactions:
        if i['trigger_serial'] == sourceSerial:
            operator = OPS[i['operator']]
            destVal = i['value']
            srcVal = data['data']

            if operator(srcVal, destVal):
                # TODO: add rips thing here
                print(i['action'])

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

# TODO: this is a filler until integrated with Rip
def readSensorData():
    return 5

def main():
    config = parseConfig()
    initLogger()

    # TODO: uncomment this for production. I don't want random webapps rn.
    #if isMaster(config['serial']):
    #    subprocess.call(['/bin/bash', '-c', './master.sh &'])
    #    # Give master time to start broker
    #    time.sleep(3)

    global conn, hardwareClient

    # Init connection to hardware library
    #hardwareClient = HardwareLibrary(parseHardwareDescription(), "")

    # TODO: Error checking. what if broker not up? Then connect fails.
    # Create mqtt client object and connect to broker
    conn = mqtt.Client(client_id='node%d' % config['serial'],
                       clean_session=True)
    conn.connect(getBrokerIp())

    # Start the async publishing loop. Manages sending mqtt network packets
    conn.loop_start()

    # Subscribe for status requests from the webapp
    topic = '%d/status_request' % config['serial']
    conn.message_callback_add(topic, handleStatusRequest)
    conn.subscribe(topic)

    # Subscribe for updates from the webapp
    conn.message_callback_add('webapp/updates', handleWebappUpdate)
    conn.subscribe('webapp/updates')

    # Subscribe for each interaction
    global interactions
    interactions = getOwnInteractions()
    for i in interactions:
        topic = '%d/data_stream' % i['trigger_serial']
        conn.message_callback_add(topic, handleInteraction)
        conn.subscribe(topic)

    # Publish sensor data for other device's interactions
    topic = '%d/data_stream' % config['serial']
    while True:
        # TODO: change this to Rip's thing
        data = {'data' : readSensorData()}

        conn.publish(topic, json.dumps(data))

        # TODO: publish heartbeats

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()

