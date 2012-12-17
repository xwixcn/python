#-*-coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ForkingMixIn,ThreadingMixIn
import time
import os
import signal
from code.SingleCompare import *
from code.MultiCompare import *
from Schedulermanager import *
from listenerhandle import Listener
from apscheduler.scheduler import Scheduler
import datetime
import json
from redisClient import *
jobnum = 0
from code.regressLogger import *
log =create_log("CompareServices")
redis=redisClient("192.168.23.76",6379,0)
class JobRequestHandler(BaseHTTPRequestHandler):
    '''
      @func:the class has two services:
      @schedlist:the scheduler object list,contains the no use scheduler object 
      @returndata:the data to write,format:
        {service_name:,jobid:,status:}
        return type is json.
     '''

    def do_GET(self):
        path = self.path
        self.send_response(200)
        self.send_header('content-type','text/plain')
        self.end_headers()
        parsed_path=path.split('/')
        service_opt=parsed_path[1]
        service_name=parsed_path[2]
        jobid=parsed_path[3]
        returndata={'jobid':jobid,"service_name":service_name,"status":""}
        schedname=jobid+"_"+service_name
        if service_opt=="job_start":
            schedlist=obj.scheduqueue
            if len(schedlist)==0:
                self.wfile.write('nosched')
                log.info("the queue is empty")
                return
            if service_name=="multicompare":
                sched=obj.getsched(0,jobid)
                exec_date=datetime.datetime.now()+datetime.timedelta(seconds=2)
                sched.add_date_job(getMultiCompareResult,exec_date,args=[jobid],name=schedname)
                returndata["status"]="pass"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
            elif service_name=="singlecompare":
                exec_date=datetime.datetime.now()+datetime.timedelta(seconds=2)
                sched=obj.getsched(0,jobid)
                sched.add_date_job(getSingleCompareResult,exec_date,args=[jobid],name=schedname)
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
                log.info(str(e))
                returndata["status"]="faild"
                returndata=json.dumps(returndata)
                self.wfile.write(returndata)
                return
        else:
            self.send_response(404)
            resp="no site to visit"
            self.wfile.write(resp)

def getMultiCompareResult( jobid ):
        '''
        获取比对结果
        '''
        sentence_name="sentences__"+jobid
        cases=redis.hkeys(sentence_name)
        if cases:
            case_result = Multicompare( cases )
        else:
            case_result=""
        redis.put_compareresult(case_result,"compare",jobid)
        return jobid
    
    
def getSingleCompareResult( jobid ):
        sentence_name="sentences__"+jobid
        cases=redis.hkeys(sentence_name)
        if cases:
            case_result = SingleCompare( cases )
        else:
            case_result=""
        redis.put_compareresult(case_result,"compare",jobid)

        return jobid


class ProcessHTTPServer(ThreadingMixIn,HTTPServer):
    """Handle requests in a separate process"""

if __name__=="__main__":
    schedlist=[]
    obj=Schedulermanger(schedlist)
    sched=Scheduler()
    listener=Listener(obj)
    sched.add_listener(listener.listener_jobfinish,64|128)
    obj.putsched(sched,sched)
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
    serv = ProcessHTTPServer(('192.168.23.75',10001),JobRequestHandler)
    serv.serve_forever()
