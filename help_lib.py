import logging
import os

LOG_FOLDER = 'logs'
LOG_FILE = '%s/node.log' % LOG_FOLDER
CONFIG_FILE = 'CONFIG'

def initLogger():
    os.system('mkdir %s' % LOG_FOLDER)
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def parseConfig():
    # Programmer forgot to init config file. Remind them.
    if not os.path.exists(CONFIG_FILE):
        raise Exception('Error: %s does not exist!' % CONFIG_FILE)

    result = dict()
    with open(CONFIG_FILE, 'r') as fp:
        for line in fp:
            # Strip newline character
            if len(line) > 0 and line[-1] == '\n':
                line = line[:-1]

            # Skip blank lines or comments
            if len(line) == 0 or line[0] == '#':
                continue

            # Programmer misformatted config file. Remind them.
            if ':' not in line:
                raise Exception('Error: %s file has option with no ":" in it'
                                % CONFIG_FILE)

            key = line.split(':')[0]
            val = line.split(':')[1]

            # Convert to bool, else convert to int
            if val == 'True':
                val = True
            elif val == 'False':
                val = False
            elif val.isdigit():
                val = int(val)
            # else: type(val) == string

            result[key] = val

    return result