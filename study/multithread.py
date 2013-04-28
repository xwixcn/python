#-*-coding:utf-8
#!/usr/bin/env python
# Simple processing example

import os
from multiprocessing import Process,current_process
import signal
import time
def f(name):
	for i in xrange(1000000):
		with open("2.txt","a+") as f:
			f.write("ss+'\n'")

if __name__ == '__main__':
    print 'Parent process:', current_process()
    p = Process(target=f, args=["sas"])
    p.start()
    print p.is_alive()
    print p.pid
    time.sleep(1)
    p.terminate()
    time.sleep(1)
    print p.is_alive()
    #os.kill(pid, signal.SIGILL)





# EOFError: EOF when reading a line