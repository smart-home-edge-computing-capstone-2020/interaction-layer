from db_lib import getOwnInteractions, getBrokerIp, isMaster
from config_parser import parseConfig
import json
import operator
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import subprocess
import time


'''
TODO
'config changes' from webapp
    add (interaction), provide all data
    delete (interaction), provide interaction id
    update (node), provide new description AND name (maybe optional and I search?)

integrate with hardware layer
interactions should be ironed out

heartbeats
master failover

DONE
nodes should respond statuses
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

# Make global so that handler functions can also publish
conn = None

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

# TODO: this is a filler until integrated with Rip
def readSensorData():
    return 5

def main():
    config = parseConfig()
    # TODO: uncomment this for production. I don't want random webapps rn.
    #if isMaster(config['serial']):
    #    subprocess.call(['/bin/bash', '-c', './master.sh &'])
    #    # Give master time to start broker
    #    time.sleep(3)

    global conn
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

    '''
    # Subscribe for config changes from the webapp
    conn.message_callback_add('config_change', doConfigChange)
    conn.subscribe('config_change')
    '''

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

