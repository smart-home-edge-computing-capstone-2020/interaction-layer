# Note: When this script is run, you should have cloned the repo found at TODO

# Set up top level modules
sudo apt-get update
sudo apt-get upgrade
#sudo apt-get install gcc # needed for psutil
#sudo apt-get install python3-devel # needed for psutil

# Install the broker
sudo apt-get install mosquitto

# Set up python virtual environment
sudo apt-get install python3-venv
python3 -m venv my_venv
source my_venv/bin/activate

# Install packages
sudo apt-get install python-pip
pip install --upgrade pip
# TODO: pip install req

# Set up the database
python3 setup_db.py

# Set up the webapp environment
sudo apt-get install npm
#TODO: Need to go do npm install and stuff, clone repos
# sudo npm install -g npm@latest
# sudo npm install

# Set up the CONFIG file TODO
# Set up the SERIAL file TODO
# Start up the node process TODO

# TODO: how to get other node's data to fill in db?
# Python libs needed:
# pgrep
# time
# os
# wheel
# paho-mqtt
