# -*- coding: utf-8 -*-
import sys
import time
import os
import hashlib
import threading
from multiprocessing import Process,Queue,Lock
from webdataUtil import webdataUtil
#from Email import sendEmail, genAttach
from config_agent import load_config
import datetime
from gen_cookie import *
import json
from regressLogger import log
from MainCompare import *
from redisClient import *


config = load_config( "compare.cfg" )
pool_size = int( config.get( '公共配置', '进程数' ) )
baseurl = config.get( '单个比对', '测试环境' )
        
lock=Lock()
    
def processcase( queue,result ):
        while(True):
            '''case=queue.get()
            case = case.strip()
            onesitedata = {}
            basecookie = get_abs_path( 'cookie/cookie.txt' )
            base_obj = webdataUtil( basecookie )
            lock.acquire()
            try:
                time.sleep( 0.2 )
                if isinstance( case, unicode ):
                    case = case.encode( 'utf-8' )
                base_data = base_obj.get_ontology_data( self.baseurl, case )
                onesitedata["md5"] = hashlib.md5( case ).hexdigest()
                onesitedata["name"] = case
                if base_data.has_key( "result" ):
                    stock_codes = [stock[0] for stock in base_data["result"]]
                    num = len( stock_codes )
                    if len( stock_codes ) == 0:
                        onesitedata["stocknum"] = 0
                        result.append(onesitedata)
                    else:
                        pass
                else:
                    onesitedata["stocknum"] = 0
                    result.append(onesitedata)
            except Exception, e:
                print e
                onesitedata["unkowon"] = 1
                result.append(onesitedata)
            lock.release()
            queue.task_done()
            '''
            if queue.empty():
                break
            print os.getpid()
            print queue.get()
          
    
def SingleCompare( cases ):
        '''
            获取一个网站数据
        '''
        result=[]
        casequeue=Queue()
        for case in cases:
            casequeue.put(case)
        procs=[Process(target=processcase,args=(casequeue,result))for i in xrange(5)]
        for p in procs:
            p.start()
        casequeue.close()
        for p in procs:
            p.join()

def get_abs_path( file ):
     return os.path.join( os.path.dirname( __file__ ), file )



if __name__=="__main__":
   cases=[x for x in xrange(100)]
   SingleCompare(cases)

        
