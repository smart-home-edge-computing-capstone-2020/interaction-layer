import logging
import os

LOG_FOLDER = 'logs'
LOG_FILE = '%s/node.log' % LOG_FOLDER

def initLogger():
    os.system('mkdir %s' % LOG_FOLDER)
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def getOwnSerial():
    # TODO: Should check if serial file exists
    with open('SERIAL', 'r') as fp:
        result = fp.readline()

    # TODO: make sure length is enough
    return result[:-1]

# TODO: do I need?
def getOwnIp():
    pass
