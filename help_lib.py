from config_parser import parseConfig
import logging
import os
from mqtt_socket import MqttSocket

def printLogFolder():
    print(parseConfig()['log_folder'])

def initLogger():
    log_folder = os.path.expanduser(parseConfig()['log_folder'])
    log_file = '%s/node.log' % log_folder
    os.system('mkdir %s' % log_folder)
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

# Note: This function only works when the broker and nodes are up
# @param serial: a list of integers representing the serial numbers to get the
#                statuses of.
def getNodeStatus(serials):
    # TODO: Error checking. what if broker not up?
    sock = MqttSocket()

    result = dict()

    for s in serials:
        listenTopic = '%d/status_response' % s
        sock.setListen(listenTopic)

        # Publish empty message to trigger response from node
        requestTopic = '%d/status_request' % s
        status = sock.getResponse(requestTopic, '{}')

        result[s] = status

    sock.cleanup()

    return result
