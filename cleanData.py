# Average data points and get rid of error messages
import glob   

def clean_data():
	path = 'output/*'   
	files = glob.glob(path)  
	dict = {} 
	for file in files:     
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

	    f = open(file, 'w')
	    for key in dict:
	    	# Average the values and output to the file
	    	val = dict[key]
	    	[float(i) for i in val]
	    	f.write(key)
	    	f.write(" ")
	    	print val
	    	f.write(str(float(sum(val))/len(val)))
	    	f.write("\n")
	    f.close()

if __name__ == "__main__":
	clean_data()
