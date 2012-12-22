#-*-coding:utf-8

import urllib2
class Listener:
    def __init__( self, scheduler ):
        self.scheduler = scheduler

    def listener_jobfinish( self, event ):
        elemlist = event.job.name.split( "_" )
        jobid = elemlist[0]
        service_name = elemlist[1]
        status = ""
        if event.exception:
           print event.exception
           status = "job_fail"
        elif event.retval == -1:
           print event.retval
           status = "job_fail"
        else:
           status = "job_finish"
        self.scheduler.resetsched( jobid )
        fullurl = "http://192.168.23.76:10000/" + status + "/" + service_name + "/" + jobid
        print fullurl
        urllib2.urlopen( fullurl )

    def listener_jobstart( self, event ):
        pass


    def listener_scheduler_shutdown( self, event ):
        pass





    

