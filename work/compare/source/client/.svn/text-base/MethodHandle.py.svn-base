#-*-coding:utf-8
from Schedulermanager import *
import datetime
class MethodHandle:

    def __init__( self, num ):
        
        self.schemanager = Schedulermanager( num )

    def init_service( self ):
        scheduqueue = self.schemanager.scheduqueue
        if scheduqueue.empty():
           return -1
        return 0 

    def exec_procedure( self, jobid, func, args, name ):
        print '开始执行任务' 
        exec_date = datetime.datetime.now() + datetime.timedelta( seconds = 2 )     
        try:
            sched = self.schemanager.getsched( jobid )
            print jobid, func, name
            sched.add_date_job( func = func, date = exec_date, args = args, name = name )
            print '启动成功'
            return 0 
        except Exception, e:
            print e
            return -1

    def stop_procedure( self, jobid ):
        try:
            if self.schemanager.useingscheddic[jobid]:
               self.schemanager.resetsched( jobid )
               result = "job成功停止"
            else:
               result = "没有正在运行的job"

        except Exception, e:
            print e
            result = "job停止失败"
        finally:
            return result
        
    def get_servicestatus( self ):
        return 'run'



