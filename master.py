import help_lib
import logging
import os
import psutil
import time

# In seconds
SLEEP_TIME = 1
MOSQUITTO_LOG_FILE = '%s/mosquitto.log' % help_lib.LOG_FOLDER

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
            # Run in background and redirect stdout and stderr to mosquitto.log
            os.system('mosquitto -d >> %s 2>&1' % MOSQUITTO_LOG_FILE)

        # Spin up webapp

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
