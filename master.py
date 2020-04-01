import help_lib
import logging
import os
import psutil
import time

# In seconds
SLEEP_TIME = 1

# TODO: remove psutil
def isRunning(name):
    for proc in psutil.process_iter():
        try:
            if name.lower() == proc.name().lower():
                return True
        except Exception as e:
            logging.error(e)
    return False

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
