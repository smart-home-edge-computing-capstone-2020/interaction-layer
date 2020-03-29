import os
import sqlite3

DB_FILENAME = 'node_data.db'
    
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
            is_sensor integer,
            is_device integer,
            is_master integer,
            is_broker integer,
            is_up integer,
            last_up integer
            );''')

    c.execute(
        '''CREATE table transactions (
            source_serial integer,
            operator text,
            value integer,
            dest_serial integer,
            action text
            );''')

    # Save changes
    conn.commit()
    conn.close()

# Run as a script
if __name__ == '__main__':
    main()
