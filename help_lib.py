from config_parser import parseConfig
from db_lib import getColNames, getBrokerIp, isUp
import json
import logging
import os
from mqtt_socket import MqttSocket
import paho.mqtt.publish as publish

def printLogFolder():
    log_folder = parseConfig()['log_folder']
    print(os.path.expanduser(log_folder))

def initLogger():
    log_folder = os.path.expanduser(parseConfig()['log_folder'])
    log_file = '%s/node.log' % log_folder
    os.system('mkdir %s' % log_folder)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

# Note: This function only works when the broker and nodes are up
# @param serial: a list of integers representing the serial numbers to get the
#                statuses of.
# @return: a dictionary mapping key = serial to value = a dict
#          the inner dict is of the form {'status' : str}
def getNodeStatus(serials):
    initLogger()
    # TODO: Error checking. what if broker not up?
    sock = MqttSocket()

    result = dict()

    for s in serials:
        logging.info('Webapp requested status of node %d' % s)
        if not isUp(s):
            result[s] = {'status' : '-1'}
            logging.info('Node %d is dead, not requesting' % s)
            continue

        listenTopic = '%d/status_response' % s
        sock.setListen(listenTopic)

        # Publish empty message to trigger response from node
        requestTopic = '%d/status_request' % s
        logging.info('Node %d is up, sending status request' % s)
        status = sock.getResponse(requestTopic, '{}')

        result[s] = '-1' if status is None else status

    sock.cleanup()
    logging.info('Status request result: %s' % str(result))

    return result

# @param serial: serial (int) number of the device to set the status of
#                statuses of.
# @param status: the status, as a string.
def setNodeStatus(serial, status):
    payload = {'status': status}
    publish.single(topic='%d/status_change_request' % serial,
                   hostname=getBrokerIp(),
                   payload=json.dumps(payload))

# @param vals: a dict mapping col name to col value. All columns must be present
#              excpet for interaction_id. See README.md for columns.
def addInteraction(vals):
    # Validate input
    neededColNames = set(getColNames('interactions'))
    neededColNames.remove('interaction_id')
    givenColNames = set(vals.keys())
    if len(neededColNames.difference(givenColNames)) != 0:
        raise Exception('Error: addInteraction called with incorrect columns: '
                        + str(vals.keys()))

    payload = {'type': 'add',
               'table': 'interactions',
               'vals': vals}
    publish.single(topic='webapp/updates',
                   hostname=getBrokerIp(),
                   payload=json.dumps(payload))

# @param interaction_id: the interaction to delete
def deleteInteraction(interaction_id):
    payload = {'type': 'delete',
               'table': 'interactions',
               'interaction_id': interaction_id}
    publish.single(topic='webapp/updates',
                   hostname=getBrokerIp(),
                   payload=json.dumps(payload))

# @param interaction_id: the interaction to delete
# @param vals: a dict mapping col name to col value. All columns must be present
#              excpet for interaction_id. See README.md for columns.
def updateInteraction(interaction_id, vals):
    # Validate input
    neededColNames = set(getColNames('interactions'))
    neededColNames.remove('interaction_id')
    givenColNames = set(vals.keys())
    if len(neededColNames.difference(givenColNames)) != 0:
        raise Exception('Error: updateInteraction called with incorrect columns: '
                        + str(vals.keys()))

    payload = {'type': 'update',
               'table': 'interactions',
               'interaction_id': interaction_id,
               'vals': vals}
    publish.single(topic='webapp/updates',
                   hostname=getBrokerIp(),
                   payload=json.dumps(payload))

# @param vals: a dict containing only 'display_name' and 'description'
def updateNode(serial, vals):
    if len(vals) != 2 or 'display_name' not in vals or 'description' not in vals:
        raise Exception('Error: updateNode called with incorrect columns: '
                        + str(vals.keys()))

    payload = {'type': 'update',
               'table': 'node_data',
               'serial': serial,
               'vals': vals}
    publish.single(topic='webapp/updates',
                   hostname=getBrokerIp(),
                   payload=json.dumps(payload))
