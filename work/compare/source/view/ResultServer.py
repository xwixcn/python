#-*-coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ForkingMixIn,ThreadingMixIn
import time
import os
from code.MainCompare import *
from code.unit import postData
from Schedulermanager import *
from listenerhandle import Listener
from apscheduler.scheduler import Scheduler
import datetime
import json
from redisClient import *
from code.regressLogger import *
log=create_log("ResultService")
jobnum = 0
redis=redisClient("192.168.23.76",6379,0)
class JobRequestHandler(BaseHTTPRequestHandler):
    '''
      @func:the class has two services:
        1:multicompare:to compare between to envs according to the config.
        2.singlecompare:to determine whether the data exists under      the the specified environment 
      @schedlist:the scheduler object list,contains the no use scheduler object 
      @returndata:the data to write,format:
        {service_name:,jobid:,status:}
        return type is json.
     '''
    def __update_job_num(self,opt,pid):
        job_record_file = open('job.record','aw')
        if opt == 'add':
            job_record_file.write(str(pid) + '\n')
            job_record_file.close()

    def do_GET(self):
        path = self.path
        self.send_response(200)
        self.send_header('content-type','text/plain')
        self.end_headers()
        parsed_path=path.split('/')
        service_opt=parsed_path[1]
        service_name=parsed_path[2]
        jobid=parsed_path[3]
        schedname=jobid+"_"+service_name
        returndata={'jobid':jobid,"service_name":service_name,"status":""}
        if service_opt=="job_start":
            exec_date=datetime.datetime.now()+datetime.timedelta(seconds=2)
            myqueue=obj.scheduqueue
            print jobid
            if len(myqueue)==0:
                returndata["status"]="faild"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
            if service_name=="result":
                sched=obj.getsched(0,jobid)
                sched.add_date_job(postresultdata,exec_date,args=[jobid],name=schedname)
                returndata["status"]="pass"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
            else:
                 self.send_response(404)
                 self.wfile.write('no site to visit')
                 return
        elif service_opt=="job_stop":
            try:
                obj.resetsched(jobid)
                returndata["status"]="pass"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return 
            except Exception,e:
                returndata["status"]="faild"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
        else:
            self.send_response(404)
            resp="no site to visit"
            self.wfile.write(resp)

def postresultdata( jobid):
        '''
        post result 
        '''
        #case_result = redis.get_compareresult(service_result,jobid)
        service_name="compare"
        case_result = redis.get_compareresult(service_name,jobid)
        postData(case_result)
        return jobid
    
    
class ProcessHTTPServer(ThreadingMixIn,HTTPServer):
    """Handle requests in a separate process"""

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
    path=os.getcwd()
    try:
        pid=os.fork()
        if pid>0:
            print 'mypid is %s'%(pid)
            sys.exit(1)
    except OSError,e:
        sys.exit(1)
    os.chdir(path)
    os.setsid()
    os.umask(0)
    serv = ProcessHTTPServer(('192.168.23.75',10002),JobRequestHandler)
    serv.serve_forever()
