# Interaction Layer
The interaction layer consists of the following programs:
Master
Node
Broker

Note that the master and node processes require the existence of a CONFIG
file of the following format:
{
    serial: unsigned integer, unique
    db_filename: path to where the db file should be (including file name)
    log_folder: path to where the logs should be stored (including folder name)
}

Since the serial number must be unique, this file is not committed, and must be
manually created on each new node.

## Database

The database stores the following information:
- sensor data
- node data
    - serial number
    - ip address
    - master status
    - broker status (at the current implementation, master and broker are the
      same node. this differentiation is put in place in case in the future,
      master and broker nodes are separated.)
    - is_up (whether the node is alive or not) (todo: should this be in heartbeat table?)
    - timestamp of last alive
      note that the above 2 together create a "heartbeat"
    - display name (name shown to user on the webapp)
    - description (defined by user on the webapp)
- stored interactions

Note that all the nodes in the network will not necessarily have identical
sqlite databases. Of the above information, only node data and defined
interactions should be synced across nodes. sensor data will be stored
exclusively on the node that gathered the data. Similarly, subscribed channels
will be stored only on the node that is subscribing.

Another thing to note is that subscribed channels is not something contained in
the database. This is because subscribed channels can be figured out based off
of implementation and the other information stored in the database.

SQLite does not support booleans. As such, they are represented integers where
0 is false and 1 is true.

As a result, each node's database will have the following tables:

#### sensor\_data
| Timestamp (key)          | Value |
| :----------------------: | :---: |
| int, seconds since epoch | int   |

#### node\_data
| serial (key)     | ip\_address | is\_master | is\_broker | is\_device | is\sensor | is\_up | last\_up                 | display\_name | description |
| :-------------:  | :---------: | :--------: | :--------: | :--------: | :-------: | :----: | :----------------------: | :-----------: | :---------: |
| int              | text        | bool       | bool       | bool       | bool      | bool   | int, seconds since epoch | text          | text        |

#### interactions
| trigger\_serial | operator | value | target\_serial | action | display\_name | description |
| :-------------: | :------: | :---: | :------------: | :----: | :-----------: | :---------: |
| int             | text     | int   | int            | text   | text          | text        |

Note: The key in the interactions layer (referred to as the interaction ID)
      is the automatically generated sql key for the entry.
Note: In the interactions table, operator is one of {'<', '<=', '==', '>', '>=}
<br>E.g. "if trigger < 5 then target action"
<br>In this case, if the sensor data published by the trigger node is <5, the target node will do "action"

## MQTT
The interaction layer uses an MQTT broker to manage communications. You can find
out more about mqtt
[here](https://www.hivemq.com/mqtt-essentials/)
and about mqtt topics
[here](https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/).
In particular, the broker used is
[mosquitto](https://mosquitto.org/)
and the backend python library used as a client is
[paho-mqtt](https://www.eclipse.org/paho/clients/python/docs/).

In addition, you have to make sure that the device running the broker (most
likely an AWS instance) has port 1883 open, as that is the one that the broker
listens on.

#### Broker Topics
The topics used in this system are broken up below by each separate subsystem,
and whether that subsystem is publishing or subscribing to the topic.
- webapp
    - publish
        - webapp/updates
            - Updates such as changing description of a node or adding a new
              interaction.
        - {node_serial_num}/status_request
            - Ask a node for its status
    - subscribe
        - {node_serial_num}/status_response
            - Get a node's status after publishing to
              {node_serial_num}/status_request
- master
    - publish (TODO: Does the master even need to access the broker?)
    - subcribe
- node
    - publish
        - heartbeats
        - {node_serial_num}/data_stream
            - For interactions.
        - {node_serial_num}/status_response
            - Respond to webapp with this node's status
    - subscribe
        - heartbeats
        - webapp/updates
            - Updates such as changing description of a node or adding a new
              interaction.
        - {node_serial_num}/data_stream
            - For interactions.
        - {node_serial_num}/status_request
            - Webapp is requesting this node's status
