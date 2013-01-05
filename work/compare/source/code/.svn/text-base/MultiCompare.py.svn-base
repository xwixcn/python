# -*- coding: utf-8 -*-
import sys
import time
import os
import threading
from multiprocessing import Process, Manager, Pool, cpu_count
from webdataUtil import webdataUtil
from config_agent import load_config
import datetime
from gen_cookie import *
import json
from regressLogger import * 
import hashlib
from gen_cookie import gen_cookie
import sys
sys.path.append( "../client/" )
from redisClient import redisClient
def compare( case ):
        print case
        redis_1.appendjoboutput( jobid, case + "!" );
        '''
                作用:比较基础数据和测试数据结果
        '''
        if isinstance( case, unicode ):
                case = case.encode( 'utf-8' )
        base_data = base_obj.get_ontology_data( baseurl, case )
        test_data = base_obj.get_ontology_data( testurl, case )
        case_md5 = hashlib.md5( case ).hexdigest()
        bench_env = baseurl.lstrip( "http://" )
        test_env = testurl.lstrip( "http://" )
        case_result = {"name":case, bench_env:"" , \
                test_env:"" , "reason":"" }
        if base_data["result"]:
            base_stocks_len = str( len( [stock[0] for stock in base_data["result"]] ) )
        else:
            base_stocks_len = str( 0 )
        if test_data["result"]:
            test_stocks_len = str( len( [stock[0] for stock in test_data["result"]] ) )
        else:
            test_stocks_len = str( 0 )
        if cmp( base_stocks_len, test_stocks_len ) != 0:
            case_result["reason"] = bench_env + ":" + base_stocks_len + ".\n" + test_env + ":" + test_stocks_len
        finalresult = {}
        if case_result["reason"]:
            finalresult["name"] = case_result["name"]
            case_result.pop( "name" )
            detail = ""
            finalresult["detail"] = case_result["reason"]
            return finalresult



def Multicompare( job_id, cases ):
        '''
                作用:主的比对程序
        '''
        global baseurl, testurl, base_obj, test_obj, jobid, redis_1
        jobid = job_id
        redis_1 = redisClient( "192.168.23.76", 6379, 1 )
        config = load_config( "compare.cfg" )
        pool_size = int( config.get( '公共配置', '进程数' ) )
        baseurl = config.get( '多个比对', '基准环境' )
        testurl = config.get( '多个比对', '测试环境' )
        gen_cookie( baseurl )
        gen_cookie( testurl )
        basecookie = baseurl.lstrip( "http://" ) 
        testcookie = testurl.lstrip( "http://" ) 
        base_obj = webdataUtil( basecookie )
        print base_obj
        test_obj = webdataUtil( testcookie )
        print test_obj
        result = {}
        if len( cases ) == 0:
            result["total"] = 0
            result["pass"] = 0
            result["fail"] = 0
            result["unknown"] = 0
            return result
        process_pool_2 = Pool( pool_size )
        print process_pool_2
        presult = list( process_pool_2.map( compare, cases, len( cases ) / pool_size ) )
        process_pool_2.close()
        process_pool_2.join()
        resultlist = []
        for elem in presult:
            if elem:
                resultlist.append( elem )
        result["result"] = resultlist
        result["total"] = len( cases )
        result["pass"] = len( cases ) - len( resultlist )
        result["fail"] = len( resultlist )
        return result
    

def get_abs_path( file ):
     return os.path.join( os.path.dirname( __file__ ), file )



if __name__ == "__main__":
       pass 
