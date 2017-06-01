#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=30
iperf_port=5001

for min_rto in 1000; do
	for interburst_period in 0.4 0.45 0.5 0.7 0.8 1.0 1.2; do
		for qsize in 4; do
			for i in 1; do
			    echo "Running cs244 PA3 for queue size $qsize :)"
			    sudo mn --clean
			    dir=data-q$qsize-p$interburst_period-i$i
			    python topology.py --dir $dir --t $time --maxq $qsize --burst_period $interburst_period --min_rto $min_rto

			    # Need iperf running on the port specified at the top of the file for cwnd
			    python plot_tcpprobe.py -f $dir/cwnd.txt -o $dir/cwnd-iperf.png -p $iperf_port
			    # Need qmon for q.png
			    python plot_queue.py -f $dir/q.txt -o $dir/q.png
			done
		done
	done
done

./findThroughputs.sh
python cleanData.py