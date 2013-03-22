#-*-coding:utf-8
#!/usr/bin/python
"""
author:louhaibin
createtime:2013.3.14
"""


from optparse import OptionParser  

def main():  
	usage = "usage: %prog [options] arg"  
	parser = OptionParser(usage)  
	parser.add_option("-f", "--file", dest="filename",  
	                       help="read data from FILENAME",default="fime.txt")  
	parser.add_option("-v", "--verbose",  
	                       action="store_true", dest="verbose",default=11)  
	parser.add_option("-q", "--quiet",  
	                      action="store_false", dest="verbose")  

	(options, args) = parser.parse_args() 
	if options.verbose:  
		print "reading %s..." % options.filename  
 
  
if __name__ == "__main__":  
	main()  

