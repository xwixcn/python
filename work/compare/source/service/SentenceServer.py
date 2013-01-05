#!/usr/bin/env python
#-*- coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import sys
sys.path.append( "../code/" )
sys.path.append( "../client/" )
import unit as unit
import datetime
import os
from  MethodHandle import MethodHandle
from redisClient import redisClient
class GetHandler( BaseHTTPRequestHandler ):
     '''
      @func: the sentences service,to get sentences,and insert into redis
      @schedlist:the scheduler object list,contains the no use scheduler object 
      @returndata:the data to write,format:
        {service_name:,jobid:,status:}
        return type is json.
     '''
     def do_GET( self ):
        path = self.path
        self.send_response( 200 );
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
            if service_name == "sentences":
                methodhandle.exec_procedure( jobid, getcase, [jobid] , jobname )
                return
        
        elif service_opt == "job_stop":
            jobid = parsed_path[3] 
            result = methodhandle.stop_procedure( jobid )
            self.wfile.write( result )
            return
        
        elif service_opt == "job_status":
            resp = "run"
            self.wfile.write( resp )

def getcase( jobid ):
    redis_1 = redisClient( "192.168.23.76", 6379, 1 )
    ( status, msg ) = unit.getCases()
    print '获取问句...'
    if status == 0:
        for x in msg:
            redis_1.appendjoboutput( jobid, x + "!" );
    else:
        print '获取问句失败'
        
    redis = redisClient( "192.168.23.76", 6379, 0 )
    redis.put_sentences( msg, status, "sentences", jobid )
    print status
    return status 

class ProcessHTTPServer( ThreadingMixIn, HTTPServer ):
        """Handle requests in a separate thread."""

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
    server = ProcessHTTPServer( ( '192.168.23.75', 10000 ), GetHandler )
    server.serve_forever()
   
  



