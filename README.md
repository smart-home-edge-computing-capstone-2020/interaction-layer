# Interaction Layer
The interaction layer consists of the following programs:
Master
Node
Broker

Note that the master and node require the existence of a CONFIG file of the
following format:
{
    serial: unsigned integer, unique
    sensor: boolean, whether node produces sensing data
    device: boolean, whether node actuates physical changes (e.g. light on/off)
}

Since the serial number must be unique, this file is not committed, and must be
manually created on each new node.

## Database

The database has to store the following information:
- sensor data
- node data
    - serial number
    - whether it's a sensor
    - whether it's a device
    - ip address
    - master status
    - broker status (at the current implementation, master and broker are the
      same node. this differentiation is put in place in case in the future,
      master and broker nodes are separated.)
    - alive (whether the node is up or not) (todo: should this be in heartbeat table?)
    - timestamp of last alive
      note that the above 2 together create a "heartbeat"
- stored transactions

note that all the nodes in the network will not necessarily have identical
sqlite databases. of the above information, only node data and defined
transactions should be synced across nodes. sensor data will be stored
exclusively on the node that gathered the data. Similarly, subscribed channels
will be stored only on the node that is subscribing.

Another thing to note is that subscribed channels is not something contained in
the database. This is because subscribed channels can be figured out based off
of implementation and the other information stored in the database.

As a result, each node's database will have the following tables:

SQLite does not support booleans. As such, they are represented integers where
0 is false and 1 is true.

#### sensor\_data
| Timestamp (key)          | Value |
| :----------------------: | :---: |
| int, seconds since epoch | int   |


#### node\_data
| serial (key) | ip\_address | is\_sensor | is\_device | is\_master | is\_broker | is\_up | last\_up                 |
| :-------------:  | :---------: | :--------: | :--------: | :--------: | :--------: | :----: | :----------------------: |
| int              | text        | bool       | bool       | bool       | bool       | bool   | int, seconds since epoch |

#### transactions
| source\_serial | operator | value | dest\_serial | action |
| :------------: | :------: | :---: | :----------: | :----: |
| int            | text     | int   | int          | text   |

Note: In the transactions table, operator is one of {'<', '<=', '==', '>', '>=}
<br>E.g. "if source < 5 then dest action"
<br>In this case, if the sensor data published by the source node is <5, the dest node will do "action"

## MQTT
The interaction layer uses an MQTT broker to manage communications. You can find
out more about mqtt (and in particular mqtt topics) here (TODO). In particular,
the broker used is (TODO) and the backend python library used as a client is
(TODO).

In addition, you have to make sure that the device running the broker (most
likely an AWS instance) has port 1883 open, as that is the one that the broker
listens on.

#### Broker Topics
The topics used in this system are broken up below by each separate subsystem,
and whether that subsystem is publishing or subscribing to the topic.
- webapp
    - publish
        - config_changes
        - {node_serial_num}_data_req
    - subscribe
        - webapp
- master
    - publish (TODO: Does the master even need to access the broker?)
    - subcribe
- node
    - publish
        - heartbeats
        - {node_serial_num}_data_stream (for transactions)
    - subscribe
        - heartbeats
        - config_changes - {node_serial_num}_data_req
        - {node_serial_num}_data_stream (for transactions)


Citations:
https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
