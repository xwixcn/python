#-*-coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ForkingMixIn, ThreadingMixIn
import os
import sys
sys.path.append( "../code/" )
sys.path.append( "../client/" )
from SingleCompare import *
from MultiCompare import *
from  MethodHandle import MethodHandle
from redisClient import redisClient
redis = redisClient( "192.168.23.76", 6379, 0 )

class JobRequestHandler( BaseHTTPRequestHandler ):
    '''
      @func:the class has two services:
      @schedlist:the scheduler object list,contains the no use scheduler object 
      @returndata:the data to write,format:
        {service_name:,jobid:,status:}
        return type is json.
     '''

    def do_GET( self ):
        path = self.path
        self.send_response( 200 )
        self.send_header( 'content-type', 'text/plain' )
        self.end_headers()
        parsed_path = path.split( '/' )
        service_opt = parsed_path[1]
        if service_opt == "job_start":
            result = methodhandle.init_service()
            if result == -1:
                self.wfile.write( "no sched" )
                return
            service_name = parsed_path[2]
            jobid = parsed_path[3]
            jobname = jobid + "_" + service_name
            
            if service_name == "multicompare":
                methodhandle.exec_procedure( jobid, getMultiCompareResult, [jobid] , jobname )
                return
            elif service_name == "singlecompare":
                methodhandle.exec_procedure( jobid, getSingleCompareResult, [jobid] , jobname )
                return
            else:
                 self.send_response( 404 )
                 self.wfile.write( 'no site to visit' )
                 return
             
        elif service_opt == "job_stop":
            jobid = parsed_path[3] 
            result = methodhandle.stop_procedure( jobid )
            self.wfile.write( result )
            return
        
        else:
            resp = methodhandle.get_servicestatus()
            self.wfile.write( resp )

def getMultiCompareResult( jobid ):
        '''
        获取比对结果
        '''
        sentence_name = "sentences__" + jobid
        cases = redis.hkeys( sentence_name )
        if cases:
            case_result = Multicompare( jobid, cases )
        else:
            case_result = ""
        print '比对完成，结果为%s,\n开始向数据库插入结果' % ( case_result )
        redis.put_compareresult( case_result, "compare", jobid )
        return jobid
    
    
def getSingleCompareResult( jobid ):
        sentence_name = "sentences__" + jobid
        cases = redis.hkeys( sentence_name )
        if cases:
            case_result = SingleCompare( cases )
        else:
            case_result = ""
        print '比对完成，结果为%s,开始向数据库插入结果' % ( case_result )

        redis.put_compareresult( case_result, "compare", jobid )

        return jobid


class ProcessHTTPServer( ThreadingMixIn, HTTPServer ):
    """Handle requests in a separate process"""

if __name__ == "__main__":
    methodhandle = MethodHandle( 5 )
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit( 0 )
    except OSError, e:
        sys.exit( 1 )
    path = os.getcwd()
    os.chdir( path )
    os.setsid()
    os.umask( 0 )
    serv = ProcessHTTPServer( ( '192.168.23.75', 10001 ), JobRequestHandler )
    serv.serve_forever()
