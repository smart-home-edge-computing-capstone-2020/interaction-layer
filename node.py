import db_help 
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

#def on_hello(client, userdata, message):
#c.message_callback_add('hello', on_hello)
#c.subscribe('hello')

def main():
    # Create mqtt client object and connect to broker
    conn = mqtt.Client()
    brokerIp = db_help.getBrokerIp()
    conn.connect(brokerIp)

    # Start the asynch publishing loop. Manages sending mqtt network packets
    conn.loop_start()

    # Register config changes callback
    # Register sensor data request callback
    # Register interaction trigger callback

    while True:
        # read / publish sensor data
        # publish heartbeats
        pass

if __name__ == '__main__':
    main()
