from help_lib import parseConfig
import os
import sqlite3

DB_FILENAME = parseConfig()['db_filename']
    
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
            is_up integer,
            last_up integer,
            display_name text,
            description text
            );''')

    c.execute(
        '''CREATE table interactions (
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

# Run as a script
if __name__ == '__main__':
    main()
