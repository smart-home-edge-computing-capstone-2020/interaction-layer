from config_parser import parseConfig
import os
import sqlite3

# Use expanduser to expand ~ to the user's home directory
DB_FILENAME = os.path.expanduser(parseConfig()['db_filename'])

    
def main():
    # Start the database fresh
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)

    # Connect to db. Creates new file if no db found
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()

    c.execute(
        '''CREATE table sensor_data (
            timestamp integer PRIMARY KEY,
            value integer
            );''')

    c.execute(
        '''CREATE table node_data (
            serial integer PRIMARY KEY,
            ip_address text,
            is_master integer,
            is_broker integer,
            is_device integer,
            is_sensor integer,
            is_up integer,
            last_up integer,
            display_name text,
            description text
            );''')

    # Note: interaction_id is ommitted when adding an id. Declaring
    # interaction_id integer PRIMARY KEY creates an alias from rowid to
    # interaction_id, so that the unique rowid autogenerated by sqlite can be
    # easily accessed by the user.
    c.execute(
        '''CREATE table interactions (
            interaction_id integer PRIMARY KEY,
            trigger_serial integer,
            operator text,
            value integer,
            target_serial integer,
            action text,
            display_name text,
            description text
            );''')

    # Save changes
    conn.commit()
    conn.close()
    
    # Populate the db
    os.system('python populate_db.py')

# Run as a script
if __name__ == '__main__':
    main()
