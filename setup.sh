# Note: this script is intended for an Ubuntu vm.
# Version: Ubuntu Server 18.04 LTS (HVM), 
# AWS ami: ami-07ebfd5b3428b6f4d (64-bit x86) / ami-0400a1104d5b9caa1 (64-bit Arm)
# I recommend an aws t2.micro

# Set up top level modules
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-venv
sudo apt-get install python-pip

# Install the broker
sudo apt-get install mosquitto

# Set up python virtual environment
python3 -m venv my_venv
source my_venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Set up the database
python3 setup_db.py

# Set up the CONFIG file TODO
# Start up the node process TODO

# TODO: how to get other node's data to fill in db?
# Python libs needed:
# pgrep
# time
# os
# wheel
# paho-mqtt
