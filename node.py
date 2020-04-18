from db_lib import *
from help_lib import *
import json
import operator
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import subprocess
import time

SLEEP_TIME = 1
interactions = dict()
OPS = {"<"  : operator.lt,
       "<=" : operator.le,
       "==" : operator.eq,
       "!=" : operator.ne,
       ">=" : operator.ge,
       ">"  : operator.gt
}

def doConfigChange(client, userdata, message):
    #TODO: update global config variable
    print(message.payload.decode('utf-8'))

def serveData(client, userdata, message):
    print(message.payload.decode('utf-8'))

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

def readSensorData():
    return 5

def main():
    # TODO: spin up master first so that broker is up
    '''
    if current node is master():
        subprocess.call(['/bin/bash', '-c', './master.sh &'])
        # Give master time to start broker
        time.sleep(3)
    '''


    # TODO: Error checking. what if broker not up?
    # Create mqtt client object and connect to broker
    conn = mqtt.Client()
    conn.connect(getBrokerIp())

    # Start the async publishing loop. Manages sending mqtt network packets
    conn.loop_start()

    serial = parseConfig()['serial']
    '''
    # Subscribe for config changes from the webapp
    conn.message_callback_add('config_change', doConfigChange)
    conn.subscribe('config_change')

    # Subscribe for sensor data requests from the webapp
    if isSensor(serial):
        topic = '%d/data_request' % serial
        conn.message_callback_add(topic, serveData)
        conn.subscribe(topic)

    '''
    # Subscribe for each interaction
    global interactions
    interactions = getOwnInteractions()
    for i in interactions:
        topic = '%d/data_stream' % i['trigger_serial']
        conn.message_callback_add(topic, handleInteraction)
        conn.subscribe(topic)


    topic = '%d/data_stream' % serial
    while True:
        # TODO: change this to Rip's thing
        data = {'data' : readSensorData()}

        conn.publish(topic, json.dumps(data))

        # TODO: publish heartbeats

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
