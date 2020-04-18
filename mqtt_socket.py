import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time

# This class functions as a wrapper so that a client can easily get "linear"
# request / response patterns from another device, without having to create
# async callbacks.
# Usage:
#     sock = MqttSocket()
#     sock.setListen('node/data_response')
#     sock.getResponse('node/data_request', '{}')
#     sock.cleanup()
# Note that a user can call getResponse as many times as they want before
# cleanup. A user can also call setListen multiple times, which resets the
# listening topic to be the new value.
class MqttSocket:

    RETRY_TIME = 0.25

    # Private callback used internally
    def _oneTimeCallback(self, client, userdata, message):
        resp = json.loads(message.payload.decode('utf-8'))
        self.returnVal = resp

    def __init__(self, brokerIp):
        # Connect to the brokerjas anonymous device
        self.conn = mqtt.Client()
        self.conn.connect(brokerIp)

        # Start the async publishing loop to manage mqtt network packets
        self.conn.loop_start()

        # After the one time connection returns, should set this val
        self.returnVal = None

        # Set callback function
        self.conn.message_callback_add('#', self._oneTimeCallback)
        self.responseTopic = None
    
    # Subscribe to a topic to listen to. This is where you expect a response to
    # be sent back to you.
    # If called, it will reset the previous listening topic.
    def setListen(self, responseTopic):
        # Remove prev listening topic to set it to the new one
        if self.responseTopic is not None:
            self.conn.unsubscribe(self.responseTopic)
            
        self.conn.subscribe(responseTopic)
        self.responseTopic = responseTopic

    # Publishes requestMsg to requestTopic, then listens to the topic specified
    # in setListen.
    # Raises an exception if a listen topic has not been set.
    # Note: requestTopic should be different from responseTopic, or this
    #       probably won't do what you want.
    def getResponse(self, requestTopic, requestMsg):
        if self.responseTopic is None:
            raise Exception('You must call setListen before getResponse')

        self.conn.publish(requestTopic, requestMsg)

        while self.returnVal is None:
            time.sleep(self.RETRY_TIME)

        result = self.returnVal
        self.returnVal = None

        return result

    # The user of this class should call this after they're done with the obj
    def cleanup(self):
        self.conn.disconnect()
        self.conn.loop_stop()
