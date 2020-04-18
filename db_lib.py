from help_lib import parseConfig
import sqlite3

DB_FILENAME = parseConfig()['db_filename']
    
def getSqlResult(query):
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    result = c.execute(query).fetchall()

    conn.close()
    return result

def commitSqlQuery(query):
    # TODO: error check vals
    conn = sqlite3.connect(DB_FILENAME)
    conn.cursor().execute(query)
    conn.commit()
    conn.close()

def getColNames(table):
    # Connect to db
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    # Empty request to load table data into the cursor
    c.execute("SELECT * FROM %s" % table)
    names = [description[0] for description in c.description]

    conn.close()
    return names

def addNode(vals):
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

def addInteraction(vals):
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

def getBrokerIp():
    query = 'SELECT ip_address FROM node_data WHERE is_broker IS 1;'
    result = getSqlResult(query)

    if len(result) != 1:
        # TODO: This should be handled!
        pass
    return result[0][0]

def getBoolResult(serial, col):
    query = 'SELECT %s FROM node_data WHERE serial IS %s;' % (col, serial)
    result = getSqlResult(query)

    if len(result) != 1:
        # TODO: This should be handled!
        pass

    return result[0][0] == 1

def getOwnInteractions():
    serial = parseConfig()['serial']
    query ='''SELECT * FROM interactions WHERE target_serial IS %d''' % serial
    interactions = getSqlResult(query)

    # Turn sql result into a dict with the column names
    names = getColNames('interactions')
    result = []
    for i in interactions:
        result.append(dict(list(zip(names, i))))
    
    return result
