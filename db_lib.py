from config_parser import parseConfig
import logging
import os
import sqlite3

# Use expanduser to expand ~ to the user's home directory
DB_FILENAME = os.path.expanduser(parseConfig()['db_filename'])
    
# Helper function to perform a NON MODIFYING sql query to read data
# @return: a list of tuples, where each tuple is a matching row in the table
def getSqlResult(query):
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    result = c.execute(query).fetchall()

    conn.close()
    return result

# Helper function to perform a MODIFYING sql query to write data
def commitSqlQuery(query):
    conn = sqlite3.connect(DB_FILENAME)
    conn.cursor().execute(query)
    conn.commit()
    conn.close()

# Helper function to get the column names of a given table. Used to generate a
# dict of results, mapping column name : value
def getColNames(table):
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    # Empty request to load table data into the cursor
    c.execute("SELECT * FROM %s" % table)
    names = [description[0] for description in c.description]

    conn.close()
    return names

# THIS SHOULD NOT BE CALLED EXCEPT AT DB INITIALIZATION!
# Helper function to add a node to the database.
# This should be used when setting up the db, not really in production, since
# we aren't doing new device commissioning.
# @param vals: a dict mapping column name to value
def writeNodeToDb(vals):
    # If node exists, don't re-add
    if getNode(vals['serial']) is not None:
        logging.warning('Trying to insert duplicate node: ' + str(vals))
        return

    query = '''
        INSERT INTO node_data (serial,
                               ip_address,
                               is_master,
                               is_broker,
                               is_up,
                               last_up,
                               display_name,
                               description)
        VALUES ('%d', '%s', '%d', '%d', '%d', '%d', '%s', '%s');''' % (
           vals['serial'],
           vals['ip_address'],
           vals['is_master'],
           vals['is_broker'],
           vals['is_up'],
           vals['last_up'],
           vals['display_name'],
           vals['description'])

    commitSqlQuery(query)

# @param serial: the serial number of the node to update
# @param vals: a dict containing only 'display_name' and 'description'
def updateNodeInDb(serial, vals):
    if 'description' not in vals or 'display_name' not in vals:
        logging.warning('trying to update node in db incorrectly'
                        + str(vals))
        return

    query = '''
        UPDATE node_data
        SET description = '%s', display_name = '%s'
        WHERE serial = %d
    ''' % (vals['description'], vals['display_name'], serial)

    commitSqlQuery(query)

# Helper function to check if an interaction exists
# @param vals: a dict mapping column name to value
def interactionExists(vals):
    query = '''
        SELECT * FROM interactions WHERE
            (trigger_serial = '%d' AND
             operator = '%s' AND
             value = '%d' AND
             target_serial = '%d' AND
             action = '%s')''' % (
           vals['trigger_serial'],
           vals['operator'],
           vals['value'],
           vals['target_serial'],
           vals['action'])

    result = getSqlResult(query)

    if len(result) > 1:
        logging.error('Found duplicate interaction in db: ' + str(result))
        return True

    return len(result) == 1

def deleteInteractionFromDb(interaction_id):
    query = 'DELETE FROM interactions WHERE interaction_id IS %d'%interaction_id
    commitSqlQuery(query)

# Helper function to add an interaction to the database.
# Note that when using in production, if trigger_serial, operator, value,
# target_serial, and action all match, then teh interaction won't be added.
# @param vals: a dict mapping column name to value
def writeInteractionToDb(vals):
    # TODO: should I warn the frontend and the user?
    if interactionExists(vals):
        logging.warning('Trying to insert duplicate interaction: ' + str(vals))
        return

    query = '''
        INSERT INTO interactions (trigger_serial,
                                  operator,
                                  value,
                                  target_serial,
                                  action,
                                  display_name,
                                  description)
        VALUES ('%d', '%s', '%d', '%d', '%s', '%s', '%s');''' % (
           vals['trigger_serial'],
           vals['operator'],
           vals['value'],
           vals['target_serial'],
           vals['action'],
           vals['display_name'],
           vals['description'])

    commitSqlQuery(query)

def getMasterSerial():
    query = 'SELECT serial FROM node_data WHERE is_master IS 1;'
    result = getSqlResult(query)

    # Can't have more than 1 master!
    if len(result) > 1:
        logging.error('Found more than 1 master in db: ' + str(result))

    # No master found...
    if len(result) == 0:
        logging.error('No master found in db: ' + str(result))
        #TODO: what now? it will crash below...

    # Elem 0, col 0
    return result[0][0]

def getBrokerIp():
    query = 'SELECT ip_address FROM node_data WHERE is_broker IS 1;'
    result = getSqlResult(query)

    # Can't have more than 1 broker!
    if len(result) > 1:
        logging.error('Found more than 1 broker in db: ' + str(result))

    # No broker found...
    if len(result) == 0:
        logging.error('No broker found in db: ' + str(result))
        #TODO: what now? it will crash below...

    # Elem 0, col 0
    return result[0][0]

# Get a boolean value from the node_data table
def getBoolCol(serial, col):
    query = 'SELECT %s FROM node_data WHERE serial IS %s;' % (col, serial)
    result = getSqlResult(query)

    # Serial should be unique
    if len(result) > 1:
        logging.error('Found more than 1 node with same serial in db: ' + str(result))

    if len(result) == 0:
        logging.warning('Serial %d not found in getBoolCol for column %s.'
                        % (serial, col))
        #TODO: what now? it will crash below...

    # Elem 0, col 0
    return result[0][0] == 1

# Set a boolean value in the node_data table
def setBoolCol(serial, col, newVal):
    if col not in getColNames('node_data'):
        logging.warning('trying to update nonexistent col in node_data: '
                        + col)
        return

    query = '''
        UPDATE node_data
        SET %s = %d
        WHERE serial = %d
    ''' % (col, newVal, serial)

    commitSqlQuery(query)

def sqlResultToDict(table, query):
    serial = parseConfig()['serial']
    sqlResult = getSqlResult(query)

    # Turn sql result into a dict with the column names
    names = getColNames(table)
    result = []
    for row in sqlResult:
        result.append(dict(list(zip(names, row))))
    
    return result

def getOwnInteractions():
    serial = parseConfig()['serial']
    query ='''SELECT * FROM interactions WHERE target_serial IS %d''' % serial
    return sqlResultToDict('interactions', query)

# @return: a list of dictionaries. Each dict in the list is a node. The key is
#          the column name and the val is the column value for that node.
#
#          See the table node_data in README.md for schema,  col names, and data
#          types.
def getAllNodes():
    query = 'SELECT * FROM node_data'
    return sqlResultToDict('node_data', query)

# @return: None if serial not in db, else a single dictionary as described in
#          getAllNodes.
def getNode(serial):
    query = 'SELECT * FROM node_data WHERE serial IS %d' % serial
    result = sqlResultToDict('node_data', query)
    if len(result) == 0:
        return None
    return result[0]

# @return: same as getAllNodes, but for the interactions table.
def getAllInteractions():
    query = 'SELECT * FROM interactions'
    return sqlResultToDict('interactions', query)

# @return: same as getNode, but for the interactions table.
def getInteraction(interaction_id):
    query = 'SELECT * FROM interactions WHERE interaction_id IS %d' % interaction_id
    result = sqlResultToDict('interactions', query)

    if len(result) == 0:
        logging.warning('Tried to access nonexistent interaction with id %d'
                     % interaction_id)
        return None

    return result[0]

def isMaster(serial=None):
    if serial is None:
        serial = parseConfig()['serial']

    return getBoolCol(serial, 'is_master')
