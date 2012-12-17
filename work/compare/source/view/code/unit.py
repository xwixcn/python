#-*-coding:utf-8
import urllib2
import urllib
import json
from config_agent import *
from code.regressLogger import *
import httplib
log=create_log("unit")
config=load_config('compare.cfg')
post_sevices_url = config.get( '公共配置', '发送结果地址' )
data_sevices_url=config.get('公共配置','接收问句地址')
def getCases():
        '''
                获取case数据
        '''
        try:
            data = urllib2.urlopen( data_sevices_url ).read()
            cases = json.loads( data )["name"]
            return 0, cases
        except urllib2.HTTPError:
            errorMsg = "get cases encount HTTPError, %s" % sys.exc_info()[0]
            log.error( "sorry,can't receive data ,reason:%s" % ( errorMsg ) )
            return 1, errorMsg
        except urllib2.URLError:
            errorMsg = "get cases encount URLError, %s" % sys.exc_info()[0]
            log.error( "sorry,can't receive data ,reason:%s" % ( errorMsg ) )
            return 1, errorMsg

def postData(resultdata,url=post_sevices_url,method="POST" ):
        '''
        post Data
        '''
        resultdata = urllib.urlencode( resultdata )
        headers = {"Accept":"application/json", "Content-Type":"application/x-www-form-urlencoded"}
        req = urllib2.Request( url = url, data = "%s" % ( resultdata ), headers = headers )
        try:
            if method=="GET":
                request=post_sevices_url+"?"+resultdata
            else: 
                request=req
            urllib2.urlopen(request).read()
        except urllib2.HTTPError, e:
            log.error( "sorry,can't post data ,reason:%s" % ( str( e ) ) )
            sys.exit( 1 )
        except urllib2.URLError, e:
            log.error( "sorry,can't post data ,reason:%s" % ( str( e ) ) )
            sys.exit( 1 )




    
