#-*-coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ForkingMixIn, ThreadingMixIn
import time
import os
import signal
import sys
import datetime
import daemon
import urllib2
from jobcontrol import Jobcontrol
from client import outputclient, redisClient
import subprocess

class JobRequestHandler( BaseHTTPRequestHandler ):
    def __init__( self, *args, **kwargs ):
        BaseHTTPRequestHandler.__init__( self, *args, **kwargs )

    def do_GET( self ):
        #remove first '/' in request path
        path = self.path[1:]
        pathParam = path.split( '/' )
        service_opt = pathParam[0]
        service_name = pathParam[1]
        self.send_response( 200 )
        self.send_header( 'content-type', 'text/plain' )
        self.end_headers()
        
        if service_opt == 'job_status':
            '''
            根据jobid获取某个job的运行过程，主要调用jobcontrol里的get_status方法，然后回显
            '''
            jobid = pathParam[1]
            record = jobcontrol.get_jobstatus( jobid )
            self.wfile.write( record )
            
        elif service_opt == 'job_start':
            '''
               运行job，首先初始化需要运行的job，主要包括，判断该job名字是否有效，然后读取配置文件
            '''
            initresult = jobcontrol.init_job( service_name )
            if initresult[0] == -1:
                '''
                初始化失败，返回view失败的结果
                '''
                self.wfile.write( initresult[1] )
                return
            '''
                初始化成功，执行job,返回第一个procedure启动成功的消息
            '''
            jobid = initresult[1]
            procedure = initresult[2]
            execresult = jobcontrol.exec_procedure( jobid, procedure )
            self.wfile.write( execresult )
            
        elif service_opt == "job_fail":
            '''
                        如果接受到某个procedure执行失败的消息，那么job就失败
            '''
            jobid = pathParam[2]
            output = jobcontrol.fail_job( service_name, jobid )

        elif service_opt == "job_finish":
            '''
                        如果接受到某个procedure执行成功的消息，那么执行下一个procedure
            '''
            jobid = pathParam[2]
            procedure = Rclient.getnextprocedure( jobid )
            if not procedure:
                output = '没有procedure,job执行完毕'
                print output
                Rclient.appendjoboutput( jobid, output )
                Rclient.delruningjob( jobid )
                return
            jobcontrol.exec_procedure( jobid, procedure ) 

        elif pathParam[0] == 'job_kill':
            '''
                接受到view端传来的kill_job消息
            '''
            jobid = pathParam[1]
            result = jobcontrol.kill_job( jobid )
            print result
            return
        
        elif pathParam[0] == 'warning':
             jobcontrol.get_servicestatus( pathParam[1] )

        else:
            self.wfile.write( 'operate not supported' )
            self.wfile.close()
            return

Rclient = redisClient.Rclient( '192.168.23.76', 6379, 1 )
class jobcontrollerhttpserver( ThreadingMixIn, HTTPServer ):
    pass

if __name__ == "__main__":
    cmd=["python","jobcontrol.py"]
    jobcontrol = Jobcontrol()
    sub2=subprocess.Popen(cmd,shell=False)
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit( 0 )
    except OSError, e:
        print e
        sys.exit( 0 )
    path = os.getcwd()
    os.chdir( path )
    os.setsid()
    os.umask( 0 )
    serv = jobcontrollerhttpserver( ( '192.168.23.76', 10000 ), JobRequestHandler )
    serv.serve_forever()
