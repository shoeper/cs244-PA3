# Average data points and get rid of error messages
# and plot
# Makes 2 plots in the graphs/ directory
# One plot uses the average throughput, and the other uses the min throughpu

import glob   
import os
import plot_normalized_throughput
import re
import shutil

def clean_data():
	path = 'output/*' 
	graphDir = "graphs" 
	outDir = "cleanOutput"
	files = glob.glob(path)  
	# Remove existing graphs/ and output/ directory
	if os.path.exists(graphDir):
		shutil.rmtree(graphDir)
	os.mkdir(graphDir)
	if os.path.exists(outDir):
		shutil.rmtree(outDir)
	os.mkdir(outDir) 
	for file in files:    
	    dict = {} 
	    f = open(file, 'r')  
	    lines = f.readlines()   
	    for line in lines:
	    	splitLine = line.split()
	    	key = splitLine[0]
	    	val = splitLine[1]
	    	if "error" in val:
	    		continue

	    	if dict.has_key(key):
	    		dict[key].append(val)
	    	else:
	    		dict[key] = [val]
	    f.close() 

	    queueSize = re.search('[0-9]+', file).group(0)
	    outfileName = outDir + "/" + queueSize + ".txt"
	    minOutfileName = outDir + "/min" + queueSize + ".txt" 
	    # Right now, plots min and avg on 2 separate graphs
	    # To plot on the same graph, set minOutfileName to outfileName
	    # and then remove the rest of the code pertaining to minOutfile
	    outfile = open(outfileName, 'w')
	    minOutfile = open(minOutfileName, 'w')
	    for key in dict:
	    	# Average the values and output to the file
	    	val = dict[key]
	    	outfile.write(key)
	    	outfile.write(" ")
	    	val_floats = [float(x) for x in val]

	    	avg = sum(val_floats)/len(val_floats)
	    	outfile.write(str(avg))
	    	outfile.write("\n")

	    	# Write out the min of the values too
	    	minOutfile.write(key)
	    	minOutfile.write(" ")
	    	minVal = min(val_floats)
	    	minOutfile.write(str(minVal))
	    	minOutfile.write("\n")
	    outfile.close()
	    minOutfile.close()

	    # Find the queue size
	    # TODO: remove code below (about queueing) later for final submission?
	    # That is, we would have decided on a queue size then
	    # so we wouldn't need to create separate plots by queue size
	    plot_normalized_throughput.plot(outfileName, 1.0, graphDir + "/" + queueSize)
	    plot_normalized_throughput.plot(minOutfileName, 1.0, graphDir + "/min" + queueSize)

if __name__ == "__main__":
	clean_data()
