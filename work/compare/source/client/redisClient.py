#-*-coding:utf-8
from  redis import Redis 
import urllib2

class redisClient( Redis ):

    def __init__( self, host = "localhost", port = 6379, db = 0 ):
        self.host = host
        self.port = port
        self.db = db
        super( Redis, self ).__init__( host, port, db )

    def __put_data( self, name, key = "", value = "" ):
        if isinstance( key, dict ):
           self.hmset( name, key )
        else:
           self.hset( name, key, value )

    def put_compareresult( self, case_result, service_name, jobid ):
        compare_name = service_name + "__" + jobid
        maps = {}
        if not case_result:
            self.__put_data( compare_name )
        else:
            for item in case_result["result"]:
               sentence = item["name"]
               item.pop( "name" )
               maps[sentence] = item
            case_result.pop( "result" )
            maps["__summary"] = case_result
            self.__put_data( compare_name, maps )
        self.expire( compare_name, 60 * 60 * 12 )

    def put_sentences( self, cases, status, service_name, jobid ):
        sentence_name = service_name + "__" + jobid
        if status == 0:
            try:
                maps = dict.fromkeys( cases )
            finally:
                self.__put_data( sentence_name, maps )
        else:
            self.hset( service_name, "", "" )
        self.expire( service_name, 60 * 60 * 12 )

    
    def get_compareresult( self, service_name, jobid ):
        compare_name = service_name + "__" + jobid
        comparesult = self.hgetall( compare_name )
        if comparesult:
            tempresult = {}
            tempresult.update( eval( comparesult["__summary"] ) )
            comparesult.pop( "__summary" )
            if comparesult:
                resultlist = []
                tempdic = {}
                for key, value in comparesult.iteritems():
                    value = eval( value )
                    value["name"] = key
                    resultlist.append( value )
                tempdic["result"] = resultlist
                tempresult.update( tempdic )
            else:
                 tempresult["result"] = []
            comparesult = tempresult
        return comparesult


    def get_somekeyvalues( self, name, keys ):
        try:
            if isinstance( keys, list ):
                return self.hmget( name, keys )
            else:
                return self.hget( name, keys )
        except Exception, e:
            print e

    def getjobid( self ):    
        return self.incr( 'current_jobid' )

    def __gen_key( self, jobid, param = "" ):
        return 'jobid__' + str( jobid ) + '__' + param

    def initjobconfig( self, jobid, jobprocedure ):
        key = self.__gen_key( jobid, 'procedure' )
        if self.exists( key ):
            return
        for jp in jobprocedure:
            self.rpush( key, jp )
        self.__setexpire( key )

    def setrunningjob( self, jobid ):
        self.hset( "runningjob", jobid, "" )

    def delruningjob( self, jobid ):
        self.hdel( "runningjob", jobid )

    def getrunningjobnum( self ):
        jobnum = self.hkeys( "runningjob" )
        return jobnum

    def getnextprocedure( self, jobid ):
        key = self.__gen_key( jobid, 'procedure' )
        nextprocedure = self.lpop( key )
        self.__setrunningprocedure( jobid, nextprocedure )
        return nextprocedure

    def deljob( self, jobid ):
        key1 = self.__gen_key( jobid, 'procedure' )
        key2 = self.__gen_key( jobid, 'running' )
        self.delete( key1 )
        self.delete( key2 )
        
    def __setrunningprocedure( self, jobid, procedure ):
        key = self.__gen_key( jobid, 'running' )
        self.set( key, procedure )
        self.__setexpire( key )

    def getrunningprecedure( self, jobid ):
        key = self.__gen_key( jobid, 'running' )
        return self.get( key )
    def appendjoboutput( self, jobid, output ):
        '''
        append every stage output to redis
        output must be a string
        '''
        key = self.__gen_key( jobid, 'output' )
        self.rpush( key, output )
        self.__setexpire( key )

    def getjoboutput( self, jobid ):
        '''
        return job's output
        '''
        key = self.__gen_key( jobid, 'output' )
        output_len = self.llen( key )
        output = self.lrange( key, 0, output_len )
        return output 
    
    def __setexpire( self, key ):
        self.expire( key, 60 * 60 * 12 )

if __name__ == "__main__":
    redis = redisClient( '192.168.23.76', 6379, 0 )
    import time
    #print urllib2.urlopen('http://192.168.23.75:10000/job_start/sentences/188').read()
    #time.sleep(20)
    print urllib2.urlopen( 'http://192.168.23.75:10002/job_start/result/188' ).read()
    time.sleep( 1 )
    #print urllib2.urlopen('http://192.168.23.75:10001/job_start/singlecompare/188').read()
    #time.sleep(20)
    for i in  redis.hkeys( 'sentences__123' ):
         print i
    #print redis.get_compareresult("compare","188")
    #test={'1':'22'}

         
        
