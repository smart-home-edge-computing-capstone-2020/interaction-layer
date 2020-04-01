import help_lib
import logging
import os
import pgrep
import time

# In seconds
SLEEP_TIME = 1

def isRunning(name):
    return len(pgrep.pgrep(name)) > 0

def main():
    help_lib.initLogger()
    while True:
        # Spin up broker
        if not isRunning('mosquitto'):
            # Run in background and use config file
            # TODO: try different ports?
            os.system('mosquitto -d -c mosquitto.conf')

        # Spin up webapp

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
