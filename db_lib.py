import sqlite3
from help_lib import getOwnSerial

DB_FILENAME = 'node_data.db'
    
def addNode(vals):
    # TODO: error check vals
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    query = '''
        INSERT INTO node_data (serial,
                               ip_address,
                               is_sensor,
                               is_device,
                               is_master,
                               is_broker,
                               is_up,
                               last_up)
        VALUES ('%d', '%s', '%d', '%d', '%d', '%d', '%d', '%d');''' % (
           vals['serial'],
           vals['ip_address'],
           vals['is_sensor'],
           vals['is_device'],
           vals['is_master'],
           vals['is_broker'],
           vals['is_up'],
           vals['last_up'])

    c.execute(query)
    conn.commit()
    conn.close()
    
def getBrokerIp():
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    query = 'SELECT ip_address FROM node_data WHERE is_broker IS 1;'
    result = c.execute(query).fetchall()

    if len(result) != 1:
        # TODO: This should be handled!
        pass

    conn.close()
    return result[0][0]

def getBoolResult(serial, col):
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    
    query = 'SELECT %s FROM node_data WHERE serial IS %s;' % (col, serial)
    result = c.execute(query).fetchall()

    if len(result) != 1:
        # TODO: This should be handled!
        pass

    conn.close()
    return result[0][0] == 1

def isMaster(serial):
    return getBoolResult(serial, 'is_master')

def isSensor(serial):
    return getBoolResult(serial, 'is_sensor')

def isDevice(serial):
    return getBoolResult(serial, 'is_device')

def isUp(serial):
    return getBoolResult(serial, 'is_up')