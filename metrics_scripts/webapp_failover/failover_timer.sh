# Hardcodes static IP addresses of original master node and the node that should
# promote to master and host the website

# Monitor until node 1 goes down
while [ 1 ]
do
    # Get status from site; if down then connection refused, else 200
    status=$(curl -I http://34.233.41.49:3000/ 2> /dev/null | head -n 1 | awk '{print $2}')

    # Get seconds.nanoseconds, then cut nanoseconds -> milliseconds
    time=$(gdate +%s.%N)
    time=${time:0:14}

    if [ "$status" != "200" ]
    then
        echo "$time: First master is down. Failover beginning."
        break
    fi
done

# Monitor until node 2 comes up
while [ 1 ]
do
    # Get status from site; if down then connection refused, else 200
    status=$(curl -I http://18.208.23.252:3000 2> /dev/null | head -n 1 | awk '{print $2}')

    # Get seconds.nanoseconds, then cut nanoseconds -> milliseconds
    time=$(gdate +%s.%N)
    time=${time:0:14}

    if [ "$status" == "200" ]
    then
        echo "$time: New master is up. Failover complete"
        break
    fi
done
