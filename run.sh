#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=60
iperf_port=5001

for qsize in 15; do
    dir=bb-q$qsize

    echo "Running cs244 PA3 for queue size $qsize :)"
    dir=bb-q$qsize

    python topology.py --dir $dir --t $time --maxq $qsize

    python plot_tcpprobe.py -f $dir/cwnd.txt -o $dir/cwnd-iperf.png -p $iperf_port
    python plot_queue.py -f $dir/q.txt -o $dir/q.png
    python plot_ping.py -f $dir/ping.txt -o $dir/rtt.png
done
