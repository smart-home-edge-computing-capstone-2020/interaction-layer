### The database has to store the following information:

- Sensor data
- Node data
    - Serial number
    - Whether it's a sensor
    - Whether it's a device
    - IP address
    - Master status
    - Broker status (at the current implementation, master and broker are the
      same node. This differentiation is put in place in case in the future,
      master and broker nodes are separated.)
    - Alive (whether the node is up or not) (TODO: Should this be in heartbeat table?)
    - Timestamp of last alive
      Note that the above 2 together create a "heartbeat"
- Stored transactions

Note that all the nodes in the network will not necessarily have identical
sqlite databases. Of the above information, only node data and defined
transactions should be synced across nodes. Sensor data will be stored
exclusively on the node that gathered the data. Similarly, subscribed channels
will be stored only on the node that is subscribing.

Another thing to note is that subscribed channels is not something contained in
the database. This is because subscribed channels can be figured out based off
of implementation and the other information stored in the database.

As a result, each node's database will have the following tables:

#### sensor
| Timestamp (key)          | Value |
| :----------------------: | :---: |
| int, seconds since epoch | int   |


#### node\_data
| serial num (key) | ip\_address | is\_sensor | is\_device | is\_master | is\_broker | is\_up | last\_up                 |
| :-------------:  | :---------: | :--------: | :--------: | :--------: | :--------: | :----: | :----------------------: |
| int              | string      | bool       | bool       | bool       | bool       | bool   | int, seconds since epoch |

#### transactions
| source\_serial | operator | value | dest\_serial | action |
| :------------: | :------: | :---: | :----------: | :----: |
| int            | string   | int   | int          | string |

Note: In the transactions table, operator is one of {'<', '<=', '==', '>', '>=}
<br>E.g. "if source < 5 then dest action"
<br>In this case, if the sensor data published by the source node is <5, the dest node will do "action"
