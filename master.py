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

        # Spin up webapp backend
        if not isRunning('flask'):
            os.system('''cd ../ecp-webapp/flask-backend &&
                         source my_venv/bin/activate && 
                         FLASK_APP=api.py FLASK_ENV=development flask run &>> backend.log &''')

        # Spin up webapp frontend
        if not isRunning('node'):
            os.system('''cd ../ecp-webapp/ecp-frontend &&
                         serve -s build &>> frontend.log &''')

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()
