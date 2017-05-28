#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

from helper import avg, stdev

from monitor import monitor_qlen
import termcolor as T

import sys
import os
import math

parser = ArgumentParser(description="Bufferbloat tests")
parser.add_argument('--bw-server', '-bs',
                    type=float,
                    help="Bandwidth of server link (Mb/s)",
                    default=500)

parser.add_argument('--bw-attacker', '-ba',
                    type=float,
                    help="Bandwidth of attacker (network) link (Mb/s)",
                    default=500)

parser.add_argument('--bw-innocent', '-bi',
                    type=float,
                    help="Bandwidth of innocent (network) link (Mb/s)",
                    default=500)

parser.add_argument('--bw-bottleneck', '-bb',
                    type=float,
                    help="Bandwidth of bottleneck link (Mb/s)",
                    default=1.5)

parser.add_argument('--delay',
                    type=float,
                    help="Link propagation delay (ms)",
                    default=3)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    required=True)

parser.add_argument('--time', '-t',
                    help="Duration (sec) to run the experiment",
                    type=float,
                    default=10)

parser.add_argument('--maxq',
                    type=int,
                    help="Max buffer size of network interface in packets",
                    default=100)

parser.add_argument('--burst_period',
                    type=float,
                    help="Interburst period",
                    default=2)

parser.add_argument('--burst_duration',
                    type=float,
                    help="Interburst duration",
                    default=0.05)

# Linux uses CUBIC-TCP by default that doesn't have the usual sawtooth
# behaviour.  For those who are curious, invoke this script with
# --cong cubic and see what happens...
# sysctl -a | grep cong should list some interesting parameters.
parser.add_argument('--cong',
                    help="Congestion control algorithm to use",
                    default="reno")

# Expt parameters
args = parser.parse_args()

class BBTopo(Topo):

    def build(self, n=2):
        switch0 = self.addSwitch('s0')
        switch1 = self.addSwitch('s1')

        attacker_client = self.addHost('attacker')
        self.addLink(attacker_client, switch0, bw=args.bw_attacker, delay=args.delay)

        innocent_client = self.addHost('innocent')
        self.addLink(innocent_client, switch0, bw=args.bw_innocent, delay=args.delay)

        self.addLink(switch0, switch1, bw=args.bw_bottleneck, max_queue_size=args.maxq, delay=args.delay)

        server = self.addHost('server')
        self.addLink(server, switch1, bw=args.bw_server, delay=args.delay)

        return

# Simple wrappers around monitoring utilities.  You are welcome to
# contribute neatly written (using classes) monitoring scripts for
# Mininet!
def start_tcpprobe(outfile="cwnd.txt"):
    os.system("rmmod tcp_probe; modprobe tcp_probe full=1;")
    Popen("cat /proc/net/tcpprobe > %s/%s" % (args.dir, outfile),
          shell=True)

def stop_tcpprobe():
    Popen("killall -9 cat", shell=True).wait()

def start_qmon(iface, interval_sec=0.1, outfile="q.txt"):
    monitor = Process(target=monitor_qlen,
                      args=(iface, interval_sec, outfile))
    monitor.start()
    return monitor

def start_iperf(net, name, attack_mode):
    print "Starting iperf server..."

    server = net.get('server')
    server.popen("iperf -s -w 16m")

    client = net.get(name)
    if not attack_mode:
        client.popen("iperf -c %s -t %f" % (server.IP(), args.time))
    else:
        client.popen("python shrew.py %s %f %f %f" % (server.IP(), args.burst_period, args.burst_duration, args.time))

def start_webserver(net):
    server = net.get('server')
    proc = server.popen("python http/webserver.py", shell=True)
    sleep(1)
    return [proc]

def start_webpage_transfer(net, fetcher):
    # Measure the time it takes to complete webpage transfer
    # from h1 to h2 3 times every 5 seconds.  
    fetch_times = []
    start_time = time()
    while True:
        fetch_times.append(fetch_webpage(net, fetcher))
        now = time()
        delta = now - start_time
        if delta > args.time:
            break

    print len(fetch_times)
    print fetch_times
    print "Average web page fetch time: " + str(avg(fetch_times))
    print "Standard deviation for web page fetch time: " + str(stdev(fetch_times))

def start_ping(net, name):
    print "start_ping"
     # Measure RTTs every 0.1 second. 
    server = net.get('server')
    client = net.get(name)
    ping = client.popen('ping -i 0.1 -w %d %s > %s/ping.txt' % (args.time, server.IP(),
                args.dir), shell=True)

def fetch_webpage(net, fetcher):
    client = net.get(fetcher)
    server = net.get('server')
    cmdline = 'curl -s -w "%{time_total}\n" -o /dev/null ' + '%s/http/index.html' % (server.IP())
    cmd = client.popen(cmdline, shell=True, stdout=PIPE)
    return float(cmd.stdout.readline())

def bufferbloat():
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    os.system("sysctl -w net.ipv4.tcp_congestion_control=%s" % args.cong)
    topo = BBTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    # This dumps the topology and how nodes are interconnected through
    # links.
    dumpNodeConnections(net.hosts)
    # This performs a basic all pairs ping test.
    net.pingAll()

    # Start all the monitoring processes
    start_tcpprobe("cwnd.txt")

    # s0-eth3 and s1-eth1 work for where the queue builds up
    # s0-eth3 should be the the output interface from s0
    # onto the bottleneck link
    qmon = start_qmon(iface='s0-eth3',
                      outfile='%s/q.txt' % (args.dir))

    start_webserver(net) # Start first because webserver sleeps for one second, and 
                         # we don't want to do this after we start iperf
    start_iperf(net, 'attacker', True)
    start_ping(net, 'attacker')
    start_webpage_transfer(net, 'innocent')
    
    stop_tcpprobe()
    qmon.terminate()
    net.stop()
    # Ensure that all processes you create within Mininet are killed.
    # Sometimes they require manual killing.
    Popen("pgrep -f ping | xargs kill -9", shell=True).wait()
    Popen("pgrep -f iperf | xargs kill -9", shell=True).wait()
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    bufferbloat()