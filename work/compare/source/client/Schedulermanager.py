import threading
import time
import Queue
from apscheduler.scheduler import Scheduler
from listenerhandle import Listener 
lock = threading.Lock()
class Schedulermanager():
    
    def __init__(self,num):
        self.size=num
        self.useingscheddic={}
        self.queue=Queue.Queue(maxsize=num)
        self.jobid=None
        self.listener=Listener(self)
        self.putsched(num)
    
    def resetsched(self,jobid):
        '''
        shutdown the schecd by jobid 
        '''
        lock.acquire()
        try:
            self.useingscheddic[jobid].shutdown(shutdown_threadpool=False)        
            self.queue.put(self.useingscheddic[jobid])
            self.useingscheddic.pop(jobid)
        finally:
            lock.release()
    
    def getsched(self,jobid):
        '''
        get sched object by the index
        '''
        lock.acquire()
        try:
            sched=self.queue.get()
            self.useingscheddic[jobid]=sched         
            sched.start()
            print len(self.useingscheddic)
            #self.queue.remove(sched)
        finally:
            lock.release()
        return sched
    
    def putsched(self,num):
        '''
        put sched object into list
        '''
        lock.acquire()
        try:
            for i in range(num):
              sched=Scheduler()
              sched.add_listener(self.listener.listener_jobfinish,64|128)
              self.queue.put(sched)
        finally:
            lock.release()
    def checkschedqueue(self):
        if self.queue.empty():
            return -1
        else:
            return 0
    @property
    def useingscheddic(self):
        return self.useingscheddic

    @property
    def scheduqueue(self):
        return self.queue


        
    
    


if __name__=="__main__":
    c=Schedulermanager(5)
    print c.getsched("1")
    print c.getsched("2")
    print c.scheduqueue.qsize()




        
