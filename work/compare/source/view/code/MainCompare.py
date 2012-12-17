#!/usr/bin/env python
# -*- coding=utf-8 -*-
import urllib2
import sys
import hashlib
import json
import urllib
from config_agent import load_config
from SingleCompare import *
from MultiCompare  import *
from regressLogger import *
import unit
import time
log=create_log("MainCompare")
config = load_config( 'compare.cfg' )
'''proxy_Handle = urllib2.ProxyHandler( {"http": "http://172.20.23.205:80"} )
opener = urllib2.build_opener( proxy_Handle )
urllib2.install_opener( opener )
'''
class MainCompare():
    
    def __init__( self ):
        self.data_sevices_url = config.get( '公共配置', '接收问句地址' )
        self.post_sevices_url = config.get( '公共配置', '发送结果地址' )


    def getCases( self ):
        '''
                获取case数据
        '''
        try:
            data = urllib2.urlopen( self.data_sevices_url ).read()
            cases = json.loads( data )["name"][0:2000]
            print len( cases )
            return 0, cases
        except urllib2.HTTPError:
            errorMsg = "get cases encount HTTPError, %s" % sys.exc_info()[0]
            log.error( "sorry,can't receive data ,reason:%s" % ( errorMsg ) )
            return 1, errorMsg
        except urllib2.URLError:
            errorMsg = "get cases encount URLError, %s" % sys.exc_info()[0]
            log.error( "sorry,can't receive data ,reason:%s" % ( errorMsg ) )
            return 1, errorMsg
            
     
    def _getRoundInfo( self ):
        round_info = 1
        return round_info

    def getMultiCompareResult( self ):
        '''
        获取比对结果
        '''
        case_result = {}
        #if status is 1, cases is a string of errMsg
        ( status, cases ) = self.getCases()
        if status == 1:
            case_result["errMsg"] = cases
        elif status == 0:
            case_result = Multicompare( cases )
        return case_result 
    
    
    def getSingleCompareResult( self ):
        
        '''
                获取比对结果
        '''
        case_result = {}
        #if status is 1, cases is a string of errMsg
        ( status, cases ) = self.getCases()
        if status == 1:
            case_result["errMsg"] = cases
        elif status == 0:
            case_result = SingleCompare( cases )
        return case_result 


    def postData( self , flag ):
        '''
        post Data
        '''
        url = self.post_sevices_url
        if flag == 0:
            resultdata = self.getSingleCompareResult()
        elif flag == 1:
            resultdata = self.getMultiCompareResult()
        else:
            sys.exit( 1 )
        print resultdata
        unit.postData(resultdata,url)
        
     
if __name__ == "__main__":
    main = MainCompare()
    start=time.time()
    main.postData(1)
    end=time.time()
    durtime=end-start
    print "一共是%s"%(durtime)
       
