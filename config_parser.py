import json
import os

# Use expanduser to expand ~ to the user's home directory
CONFIG_FILE = os.path.expanduser('~/CONFIG')

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

def parseHardwareDescription():
    hardware_file = os.path.expanduser(parseConfig()['hardware_file'])
    result = ""
    with open(hardware_file, 'r') as fp:
        for line in fp:
            # Strip newline character
            if len(line) > 0 and line[-1] == '\n':
                line = line[:-1]

            # Remove spaces
            line = line.replace(' ', '')

            # json.loads requires " instead of '
            line.replace('\'', '"')

            result += line

    return result

# TODO: This is wrong - nodes can have more than one hardware
def getHardwareName():
    hardwareDescription = parseHardwareDescription()
    hardware = json.loads(hardwareDescription)['hardware'].keys()
    return list(hardware)[0]

def getHardwareType():
    name = getHardwareName()
    hd = parseHardwareDescription()
    return json.loads(hd)['hardware'][name]['valueType']
