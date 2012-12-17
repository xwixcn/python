import threading
import time
import Queue
from apscheduler.scheduler import Scheduler
lock = threading.Lock()
class Schedulermanger():
    
    def __init__(self,queue):
        
        self.useingscheddic={}
        self.queue=queue
        self.jobid=None
    
    def resetsched(self,jobid):
        '''
        shutdown the schecd by jobid 
        '''
        lock.acquire()
        try:
            self.useingscheddic[jobid].shutdown(shutdown_threadpool=False)        
            self.queue.append(self.useingscheddic[jobid])
            self.useingscheddic.pop(jobid)
        finally:
            lock.release()
    
    def getsched(self,index,jobid):
        '''
        get sched object by the index
        '''
        lock.acquire()
        try:
            sched=self.queue[index]
            self.useingscheddic[jobid]=sched         
            sched.start()
            self.queue.remove(sched)
        finally:
            lock.release()
        return sched
    
    def putsched(self,*args):
        '''
        put sched object into list
        '''
        lock.acquire()
        try:
            for i in args:
              self.queue.append(i)
        finally:
            lock.release()

    @property
    def useingscheddic(self):
        return self.useingscheddic

    @property
    def scheduqueue(self):
        return self.queue


        
    
    


if __name__=="__main__":
    pass





        
