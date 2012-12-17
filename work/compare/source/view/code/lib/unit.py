#-*-coding:utf-8
import urllib2
import urllib
import json
from config_agent import *
from regressLogger import log
import httplib
config=load_config('compare.cfg')

def getCases():
        '''
                获取case数据
        '''
        data_sevices_url=config.get('公共配置','接收问句地址')
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

def postData(resultdata,url ):
        '''
        post Data
        '''
        resultdata = urllib.urlencode( resultdata )
        headers = {"Accept":"application/json", "Content-Type":"application/x-www-form-urlencoded"}
        req = urllib2.Request( url = url, data = "%s" % ( resultdata ), headers = headers )
        try:
            print url
            print urllib2.urlopen( req ).read()
            print 'wwwww'
        except urllib2.HTTPError, e:
            log.error( "sorry,can't post data ,reason:%s" % ( str( e ) ) )
            sys.exit( 1 )
        except urllib2.URLError, e:
            log.error( "sorry,can't post data ,reason:%s" % ( str( e ) ) )
            sys.exit( 1 )

def postDataByget():
    resultdata= {"jobid":"22","service_name":"sentence","status":"2222"}
    resultdata=urllib.urlencode(resultdata)
    url="/test?"+resultdata
    print url
    conn = httplib.HTTPConnection("192.168.23.75:44444")
    conn.request("GET",url)
    res = conn.getresponse()
    print res.status,res.reason
    





    
if __name__=="__main__":
    postDataByget()
