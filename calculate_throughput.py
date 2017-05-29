import re
from helper import *

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f',
					help="throughput file to calculate",
					required=True)

args = parser.parse_args()

def calculate_throughput(fname):
	throughput = 0.0
	total_seconds = 0.0
	lines = open(fname).readlines()
	last_line = lines[len(lines) - 1]
	if ' 0.0' not in last_line:
		print "Could not find line in throughput file with aggregate throughput"
		return
	
	m = re.search('(?<=Bytes)[0-9\.\ ]+', last_line)

	if m is None:
		print 'Last line does not match the regex'
	else:
		if 'Mbits' in last_line:
			print float(m.group(0))
		elif 'Kbits' in last_line:
			print float(m.group(0)) / 1024

if __name__ == "__main__":
	calculate_throughput(args.file)


