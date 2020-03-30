from logging import *
import psutil
import time

# In seconds
SLEEP_TIME = 1

def isRunning(name):
    for proc in psutil.process_iter():
        try:
            if name.lower() == proc.name.lower():
                return True
        except Exception as e:
            log_error(e)
    return False

def main():
    while True:
        # Spin up broker
        if not isRunning('mosquitto'):
            # Run in background and redirect stdout and stderr to mosquitto.log
            os.system('mosquitto -d >> mosquitto.log 2>&1')

        # Spin up webapp

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
