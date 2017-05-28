#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=10
iperf_port=5001

for qsize in 15; do
    dir=bb-q$qsize

    echo "Running cs244 PA3 for queue size $qsize :)"
    sudo mn --clean
    dir=bb-q$qsize

    python topology.py --dir $dir --t $time --maxq $qsize

    # Need iperf running on the port specified at the top of the file for cwnd
    python plot_tcpprobe.py -f $dir/cwnd.txt -o $dir/cwnd-iperf.png -p $iperf_port
    # Need qmon for q.png
    python plot_queue.py -f $dir/q.txt -o $dir/q.png
    # Need ping for rtt
    python plot_ping.py -f $dir/ping.txt -o $dir/rtt.png
done
