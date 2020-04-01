import logging
import os

LOG_FOLDER = 'logs'
LOG_FILE = '%s/node.log' % LOG_FOLDER

def initLogger():
    os.system('mkdir %s' % LOG_FOLDER)
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def getOwnIp():
    pass
