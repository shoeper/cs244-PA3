#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=60
iperf_port=5001

for interburst_period in 0.2 0.25 0.3 0.35 0.4 0.45 0.50 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 1.0 1.2; do
	for qsize in 4; do
		for i in 1 2 3; do
		    echo "Running cs244 PA3 for queue size $qsize :)"
		    sudo mn --clean
		    dir=data-q$qsize-p$interburst_period-i$i
		    python topology.py --dir $dir --t $time --maxq $qsize --burst_period $interburst_period

		    # Need iperf running on the port specified at the top of the file for cwnd
		    python plot_tcpprobe.py -f $dir/cwnd.txt -o $dir/cwnd-iperf.png -p $iperf_port
		    # Need qmon for q.png
		    python plot_queue.py -f $dir/q.txt -o $dir/q.png
		    # Need ping for rtt
		    #python plot_ping.py -f $dir/ping.txt -o $dir/rtt.png
		done
	done
done
