# Note: When this script is run, you should have cloned the repo found at TODO

# Set up top level modules
sudo apt-get update
sudo apt-get install gcc # needed for psutil
sudo apt-get install python3-devel # needed for psutil

# Install the broker
sudo apt-get install mosquitto

# Set up python virtual environment
sudo apt-get install python-virtualenv
virtualenv -p /usr/bin/python3 ./my_venv
source my_venv/bin/activate
pip install --upgrade pip
# TODO: pip install req

# Set up the database
python3 setup_db.py

# Set up the config file TODO
# Start up the node process TODO

# TODO: how to get other node's data to fill in db?
# Python libs needed:
# psutil
# time
# os
