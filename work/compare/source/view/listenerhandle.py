#-*-coding:utf-8
from code.unit import *
from code.regressLogger import *
log=create_log("listenerhandle")
class Listener:
    def __init__(self,scheduler):
        self.scheduler=scheduler

    def listener_jobfinish(self,event):
        log.info(event.job)
        elemlist=event.job.name.split("_")
        jobid=elemlist[0]
        service_name=elemlist[1]
        returndata={"jobid":jobid,"service_name":service_name,"status":""}
        if event.exception:
           log.error(event.exception)
           self.scheduler.resetsched(jobid)
           returndata["status"]="fail"
        else:
           self.scheduler.resetsched(jobid)
           returndata["status"]="pass"
           postData(returndata,method="GET")

    def listener_jobstart(self,event):
        pass


    def listener_scheduler_shutdown(self,event):
        pass





    

