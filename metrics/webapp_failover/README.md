This directory includes the following files:
- time\_when\_down.sh: hangs, and prints timestamp when hardcoded master node is
                       running
- time\_when\_up.sh: hangs, and prints timestamp when hardcoded master node is
                     down
- failover\_timer.sh: does something similar to the above two files, and prints
                      out the time at which the first node's webapp stopped
                      being accessible, and the time when the new one became
                      available after the failover.
- failover\_times.txt: the results from failover\_timer.sh over 20 trials.
- avg\_webapp\_failover.py: average the results and print it out.

The data in this folder was collected by running 2 nodes, 1 master and one
other. Once the master was up and running, I started thefailover\_timer, then
killed the master node. The final averaged webapp failover time was __8.6683
seconds__.
