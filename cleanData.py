# Average data points and get rid of error messages
# and plot
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
	    outfile = open(outfileName, 'w')
	    for key in dict:
	    	# Average the values and output to the file
	    	val = dict[key]
	    	outfile.write(key)
	    	outfile.write(" ")
	    	val_floats = [float(x) for x in val]

	    	avg = sum(val_floats)/len(val_floats)
	    	outfile.write(str(avg))
	    	outfile.write("\n")
	    outfile.close()

	    # Find the queue size
	    # TODO: remove code below (about queueing) later for final submission?
	    # That is, we would have decided on a queue size then
	    # so we wouldn't need to create separate plots by queue size
	    plot_normalized_throughput.plot(outfileName, 1.0, graphDir + "/" + queueSize)

if __name__ == "__main__":
	clean_data()
