while [ 1 ]
do
    # Get status from site; if down then connection refused, else 200
    status=$(curl -I http://34.233.41.49:3000/ 2> /dev/null | head -n 1 | awk '{print $2}')

    # Get seconds.nanoseconds, then cut nanoseconds -> milliseconds
    time=$(gdate +%s.%N)
    time=${time:0:14}

    if [ "$status" == "200" ]
    then
        echo "$time: node is up"
        break
    fi
done
