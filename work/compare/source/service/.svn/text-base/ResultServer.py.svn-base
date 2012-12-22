#-*-coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ForkingMixIn, ThreadingMixIn
import os
import sys
sys.path.append( "../code/" )
sys.path.append( "../client/" )
from unit import postData
from  MethodHandle import MethodHandle
from redisClient import redisClient

class JobRequestHandler( BaseHTTPRequestHandler ):

    def service( self ):
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
            if service_name == "result":
                methodhandle.exec_procedure( jobid, postresultdata, [jobid] , jobname )
                return
        elif service_opt == "job_stop":
            jobid = parsed_path[3] 
            result = methodhandle.stop_procedure( jobid )
            self.wfile.write( result )
            return
        else:
            resp = "run"
            self.wfile.write( resp )

    do_GET = service
def postresultdata( jobid ):
        '''
        post result 
        '''
        redis = redisClient( "192.168.23.76", 6379, 0 )
        #case_result = redis.get_compareresult(service_result,jobid)
        service_name = "compare"
        case_result = redis.get_compareresult( service_name, jobid )
        status = postData( case_result )
        return status
    
    
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
    serv = ProcessHTTPServer( ( '192.168.23.75', 10002 ), JobRequestHandler )
    serv.serve_forever()
