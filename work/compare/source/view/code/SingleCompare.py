# -*- coding: utf-8 -*-
import sys
import time
import os
import hashlib
import threading
from multiprocessing import Process, Manager, Pool, cpu_count
from webdataUtil import webdataUtil
#from Email import sendEmail, genAttach
from config_agent import load_config
import datetime
from gen_cookie import *
import json
from code.regressLogger import *
from MainCompare import *

log=create_log("SingleCompare")
config = load_config( "compare.cfg" )
pool_size = int( config.get( '公共配置', '进程数' ) )
baseurl = config.get( '多个比对', '基准环境' )
gen_cookie(baseurl)
basecookie =  baseurl.lstrip("http://") 
base_obj = webdataUtil(basecookie)

        

def get_one_site_data(  case ):
        case = case.strip()
        onesitedata = {}
        try:
            time.sleep( 0.2 )
            if isinstance( case, unicode ):
                case = case.encode( 'utf-8' )
            base_data = base_obj.get_ontology_data( baseurl, case )
            onesitedata["md5"] = hashlib.md5( case ).hexdigest()
            onesitedata["name"] = case
            if base_data.has_key( "result" ):
                stock_codes = [stock[0] for stock in base_data["result"]]
                num = len( stock_codes )
                if len( stock_codes ) == 0:
                    onesitedata["stocknum"] = 0
                    return onesitedata
                else:
                    return None
            else:
                onesitedata["stocknum"] = 0
                return onesitedata
        except Exception, e:
            print e
            onesitedata["unkowon"] = 1
            return onesitedata
          
    
def SingleCompare( cases ):
        '''
            获取一个网站数据
        '''
        result = {}
        if len(cases)==0:
            result["total"]=0
            result["pass"]=0
            result["fail"]=0
            result["unknown"]=0
            return result
        pool = Pool( pool_size ) 
        pool_outputs = pool.map(get_one_site_data , cases, len( cases ) / pool_size ) 
        pool.close()
        pool.join()
        resultlist = []
        passnum = 0
        unkowonnum = 0
        failnum = 0
        for elem in list( pool_outputs ):
            if elem and not elem.has_key( "unkowon" ):
                resultlist.append( elem )
                failnum += 1
            elif elem and elem.has_key( "unkowon" ):
                unkowonnum += 1
            else:
                passnum += 1
        result["result"] = resultlist
        result["total"] = len( cases )
        result["pass"] = passnum
        result["fail"] = failnum
        result["unknown"] = unkowonnum
        #result = json.dumps( result )
        return result

def get_abs_path( file ):
     return os.path.join( os.path.dirname( __file__ ), file )



if __name__=="__main__":
   pass 

        
