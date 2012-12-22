#-*-coding:utf-8
from client import outputclient, redisClient
from confparser import confparser
import urllib2
import os
import time
class Jobcontrol:

    def __init__( self ):
        self.Rclient = redisClient.Rclient( '192.168.23.76', 6379, 1 )
        self.confparser = confparser()

    def exec_procedure( self, jobid, procedure ):
        '''
                执行某个job其中一个procedure
        '''
        url = self.confparser.getprecedureenv( procedure )
        fullurl = url + "/job_start" + "/" + procedure + "/" + str( jobid )
        output = '开始执行procedure:%s 请求地址为:%s...\t' % ( procedure, fullurl )
        self.Rclient.appendjoboutput( jobid, output )
        try:
            urllib2.urlopen( fullurl )
            output = "procedure:%s启动成功.." % ( procedure )
        except Exception, e:
            output = self.fail_job( procedure, jobid ) 
        self.Rclient.appendjoboutput( jobid, output )
        return output 
    
    def init_job( self, service_name ):
        '''
                初始化job的工作:
        1.判断job是否在配置文件里面配置的几个jobs里面，如果没有，返回状态码-1
        2.有的话，那就取出该job的几个procedure，放到redis里面，作为一个队列。
        3.然后取出第一个procedure,返回状态码0
        4.初始化工作完成
        
        '''
        output = "开始初始化job...\n"
        avail_jobs = self.confparser.getalljobs()
        jobid = self.Rclient.getjobid()
        if not service_name in avail_jobs:
                output += "sorry,the job does'nt exist\n"
                self.Rclient.appendjoboutput( jobid, output )
                return -1, output
        procedures = self.confparser.getjobprecedure( service_name )
        output += "本次job一共有%s个procedure需要执行:%s.\n" % ( len( procedures ), '\t'.join( procedures ) )
        self.Rclient.initjobconfig( jobid, procedures )
        procedure = self.Rclient.getnextprocedure( jobid )
        output += 'job准备完成,开始执行procedure:%s.\n' % ( procedure )
        print output
        self.Rclient.appendjoboutput( jobid, output )
        self.Rclient.setrunningjob( jobid )
        return 0, jobid, procedure

    def kill_job( self, jobid ):
        '''
                关闭job:
        1.如果该job还在运行，那么获取它正在运行的procedure
        2.停止该procedure，如果有procedure停止，那么整个job就算失败
        '''
        try:
            runningprocedure = self.Rclient.getrunningprecedure( jobid )
            url = self.confparser.getprecedureenv( runningprocedure )
            fullurl = url + "/job_stop" + "/" + runningprocedure + "/" + str( jobid )
            responsedata = urllib2.urlopen( fullurl ).read()
        except Exception, e:
             responsedata = "没有正在运行的job"
        self.Rclient.delruningjob( jobid )
        return responsedata

    def fail_job( self, service_name, jobid ):       
        '''
        job有procedure失败:
                如果有procedure失败，那么整个job就算失败。
        '''
        output = "procedure:%s执行失败，job终止.\t" % ( service_name )
        self.Rclient.appendjoboutput( jobid, output )
        print output
        self.Rclient.delruningjob( jobid )
        return output

        
    def record_joboutput( self, jobid ):
        '''
                记录job执行过程中，每个步骤的执行情况，当job完成或者退出时候，就把这些消息从redis
                里面取出，保存到文件里面
        '''
        output = self.Rclient.getjoboutput( jobid )
        outputdir = "../output/"
        if not os.path.exists( outputdir ):
            os.mkdir( outputdir )
        outputfile = outputdir + str( jobid )
        f = open( outputfile, 'w' )
        f.writelines( [i for i in output] )
        f.close()
        
    def get_jobstatus( self, jobid ):
       '''
        1.如果job还在运行的话，就从redis里面读取该job的运行状态。
        2.如果job已经停止运行，因为redis里面记录会过期，所以从文件里面读取。
       '''
       output = self.Rclient.getjoboutput( jobid )
       outputfile = "../output/" + str( jobid )
       if output:
           record = '\n'.join( output ) 
       elif os.path.exists( outputfile ):
               record = open( outputfile, 'r' ).read()
       else:
           record = 'no record about the job.'
       return record

    def get_servicestatus( self, errorservices ):
        '''
        当收到监控传来的procedure服务失败的消息：
        1.会从redis里面取出正在运行的jobs，如果没有jobs,那么暂时会忽略这个警告
        2.如果有运行的jobs，那么就会取得这些jobs里面正在运行的procedure
        3.判断这些procedure是否在这些失败的服务里面
        4。如果有在的，就中断这些jobs
        '''
        runningjobs = self.Rclient.getrunningjobnum()
        errorservices = errorservices.split( '+' )
        if runningjobs:
            for job in  runningjobs:
                procedure = self.Rclient.getrunningprecedure( job )
                if procedure in errorservices:
                    self.fail_job( procedure, job )

    def job_monitor( self ):
        '''
        用来监控procedure，如果有服务失败，那么就把这些失败的服务发送给jc
        '''
        while True:
            
            monitor = {}
            monitor["sentence"] = 10000
            monitor['singlecompare'] = 10001
            monitor['multicompare'] = 10001
            monitor['result'] = 10002
            warn = ""
            for service, port in monitor.items():
                try:
                    urllib2.urlopen( "http://192.168.23.75:%s/job_status" % ( port ) )
                except Exception , e:
                    warn += "+" + service
                warn = warn.strip( '+' )
            if warn:
                try:
                    urllib2.urlopen( 'http://192.168.23.76:10000/warning/%s' % ( warn ) ).read()
                except:
                    time.sleep( 30 )
                    continue
            time.sleep( 30 )
if __name__ == "__main__":
    a = Jobcontrol()
    #a.init_job("verify")
    #a.record_joboutput("93")
    print a.job_monitor()




