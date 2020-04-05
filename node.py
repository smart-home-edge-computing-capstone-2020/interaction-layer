from db_lib import *
from help_lib import *
import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import subprocess
import time

SLEEP_TIME = 1

def doConfigChange(client, userdata, message):
    print(message)

def serveData(client, userdata, message):
    print(message)

def readSensorData():
    return 5

def main():
    # TODO: spin up master first so that broker is up
    '''
    if isMaster():
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

    serial = getOwnSerial()
    '''
    # Subscribe for config changes from the webapp
    conn.message_callback_add('config_change', doConfigChange)
    conn.subscribe('config_change')

    # Subscribe for sensor data requests from the webapp
    if isSensor(serial):
        topic = '%s/data_request' % serial
        conn.message_callback_add(topic, serveData)
        conn.subscribe(topic)

    # Subscribe for each interaction
    ????
    '''

    topic = '%s/data_stream' % serial
    while True:
        data = dict()
        data['serial'] = serial

        # TODO: change this to Rip's thing
        data['data'] = readSensorData()

        conn.publish(topic, json.dumps(data))

        # TODO: publish heartbeats

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
