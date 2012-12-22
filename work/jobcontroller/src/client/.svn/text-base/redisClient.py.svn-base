#! /usr/bin/env python
# -*- coding: utf-8 -*-
from redis import Redis

class Rclient(Redis):
    def __init__(self,host,port,db):
        Redis.__init__(self,host,port,db)

    def getjobid(self):    
        return self.incr('current_jobid')

    def __gen_key(self,jobid,param=""):
        return 'jobid__' + str(jobid) + '__' + param

    def initjobconfig(self,jobid,jobprocedure):
        key = self.__gen_key(jobid,'procedure')
        if self.exists(key):
            return
        for jp in jobprocedure:
            self.rpush(key,jp)
        self.__setexpire(key)

    def setrunningjob(self,jobid):
        self.hset("runningjob",jobid,"")

    def delruningjob(self,jobid):
        self.hdel("runningjob",jobid)

    def getrunningjobnum(self):
        jobnum=self.hkeys("runningjob")
        return jobnum

    def getnextprocedure(self,jobid):
        key = self.__gen_key(jobid,'procedure')
        nextprocedure = self.lpop(key)
        self.__setrunningprocedure(jobid,nextprocedure)
        return nextprocedure

    def deljob(self,jobid):
        key1=self.__gen_key(jobid,'procedure')
        key2=self.__gen_key(jobid,'running')
        self.delete(key1)
        self.delete(key2)
        
    def __setrunningprocedure(self,jobid,procedure):
        key = self.__gen_key(jobid,'running')
        self.set(key,procedure)
        self.__setexpire(key)

    def getrunningprecedure(self,jobid):
        key = self.__gen_key(jobid,'running')
        return self.get(key)
    def appendjoboutput(self,jobid,output):
        '''
        append every stage output to redis
        output must be a string
        '''
        key = self.__gen_key(jobid,'output')
        self.rpush(key,output)
        self.__setexpire(key)

    def getjoboutput(self,jobid):
        '''
        return job's output
        '''
        key = self.__gen_key(jobid,'output')
        output_len = self.llen(key)
        output = self.lrange(key,0,output_len)
        return output 
    
    def __setexpire(self,key):
        self.expire(key,60*60*12)

if __name__ == '__main__':
    client = Rclient('192.168.23.76',6379,1)
    jobid = client.getjobid()
    from confparser import confparser
    cfg = confparser()
    #procedure = cfg.getjobprecedure('verify')
    #client.initjobconfig(jobid,procedure)
    print client.hkeys("runningjob")
    #client.appendjoboutput(jobid,'aaa')
    #print client.getjoboutput(jobid)
