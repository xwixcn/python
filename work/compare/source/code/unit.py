#-*-coding:utf-8
import urllib2
import urllib
import json
from config_agent import *
import httplib
import traceback
def getCases():
        '''
                获取case数据
        '''
        config = load_config( 'compare.cfg' )
        data_sevices_url = config.get( '公共配置', '接收问句地址' )
        try:
            data = urllib2.urlopen( data_sevices_url ).read()
            Cases = json.loads( data )
            cases = [result["name"] for result in Cases]
            return 0, cases
        except urllib2.HTTPError:
            errorMsg = "get cases encount HTTPError, %s" % sys.exc_info()[0]
            return -1, errorMsg
        except urllib2.URLError:
            errorMsg = "get cases encount URLError, %s" % sys.exc_info()[0]
            return -1, errorMsg

def postData( resultdata, url = "", method = "POST" ):
        '''
        post Data
        '''
        config = load_config( 'compare.cfg' )
        post_sevices_url = config.get( '公共配置', '发送结果地址' )
        resultdata = urllib.urlencode( resultdata )
        if not url:
            url = post_sevices_url
        headers = {"Accept":"application/json", "Content-Type":"application/x-www-form-urlencoded"}
        try:
            req = urllib2.Request( url = url, data = "%s" % ( resultdata ), headers = headers )
            if method == "GET":
                request = post_sevices_url + "?" + resultdata
            else: 
                request = req
            print request
            urllib2.urlopen( request )
            return 0
        except urllib2.HTTPError, e:
            print e.read()
            print traceback.format_exc()
            return -1
        except urllib2.URLError, e:
            print e
            return -1



    
