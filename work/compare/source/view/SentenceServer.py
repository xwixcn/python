#!/usr/bin/env python
#-*- coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn,ForkingMixIn
from code.config_agent import *
import urllib2
import json
import sys
import code.unit as unit
import time
import subprocess
from apscheduler.scheduler import Scheduler
import Queue
from Schedulermanager import *
from  listenerhandle import *
import datetime
from redisClient import redisClient
from code.regressLogger import *
sys.path.append( "code/compare.cfg" )
config=load_config('compare.cfg')
log=create_log("SentenceService")
redis=redisClient("192.168.23.76",6379,0)
class GetHandler(BaseHTTPRequestHandler):
     '''
      @func: the sentences service,to get sentences,and insert into redis
      @schedlist:the scheduler object list,contains the no use scheduler object 
      @returndata:the data to write,format:
        {service_name:,jobid:,status:}
        return type is json.
     '''
     def do_GET(self):
        path=self.path
        self.send_response(200);
        self.send_header('content-type','text/plain')
        self.end_headers()
        parsed_path=path.split('/')
        jobid=parsed_path[3]
        service_name=parsed_path[2]
        service_opt=parsed_path[1]
        jobname=jobid+"_"+service_name
        returndata={
                    "jobid":jobid,
                    "service_name":service_name,
                    "status":""
                    }

        if service_name=="sentences" and service_opt=="job_start":
            schedlist=obj.scheduqueue
            if len(schedlist)==0:
                self.wfile.write('nosched')
                return
            exec_date=datetime.datetime.now()+datetime.timedelta(seconds=2)
            sched=obj.getsched(0,jobid)
            sched.add_date_job(getcase,exec_date,args=[jobid],name=jobname)
            returndata["status"]="pass"
            returndata=json.dumps(returndata)
            self.wfile.write(returndata)
            return
        elif service_name=="sentences" and service_opt=="job_stop":
            try:
                obj.resetsched(jobid)
                returndata["status"]="pass"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
            except Exception,e:
                log.info(str(e))
                returndata["status"]="faild"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
        else:
            self.send_response(404)
            resp="no site to visit"
            self.wfile.write(resp)

def getcase(jobid):
    (status,msg)=unit.getCases()
    print msg 
    redis.put_sentences(msg,status,"sentences",jobid)
    return jobid

class ProcessHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

if __name__=="__main__":
    schedlist=[]
    obj=Schedulermanger(schedlist)
    sched=Scheduler()
    listener=Listener(obj)
    sched.add_listener(listener.listener_jobfinish,64|128)
    obj.putsched(sched)
    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)
    except OSError,e:
        sys.exit(1)
    path= os.getcwd()
    try:
        pid=os.fork()
        if pid>0:
            print 'mypid is %s'%(pid)
            sys.exit(0)
    except OSError,e:
        sys.exit(1)
    os.chdir(path) 
    os.setsid() 
    os.umask(0)
    server=ProcessHTTPServer(('192.168.23.75',10000),GetHandler)
    server.serve_forever()
   
  



