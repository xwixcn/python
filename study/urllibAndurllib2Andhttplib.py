#!/usr/bin/python
#-*-coding:utf-8
#urllib,urllib2,httplib Test
#author:louhaibin
import urllib2
import urllib
import httplib
import os
import cooklib
import socket
class Test_urllib( object ):

    def __init__( self, url ):
        self.url = url

    def use_urltriver( self ):
        filepath = os.path.join( os.path.abspath( "./" ), "a.html" )
        print filepath
        urllib.urlretrieve( self.url, filepath )


class Test_urllib2( object ):
    
    def __init__( self, url ):
        self.url = url
    #最简单方式
    def use_urllib2( self ):
        try:
            f = urllib2.urlopen( self.url ).read()
        except urllib2.URLERROR, e:
            print e.reason
        print len( f )
    #使用Request
    def use_Request( self ):
        #设置超时
        socket.setdefaulttimeout( 5 )
        #加入参数[无参数，使用get]
        params = {"wd":"a", "b":"2"}
        i_headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                "Accept":"text/plain"}
        req = urllib2.Request( url = self.url, headers = i_headers )
        try:
            f = urllib2.urlopen( req ).read()
        except urllib2.URLERROR, e:
            print e.reason()
        except urllib2.HTTPERROR, e:
            print e.reason()

        print len( f )

    def use_Proxy( self ):
        enable_proxy = True
        proxy_handle = urllib2.ProxtHandler( {"http":'http://'} )
        null_proxy_handle = urllib2.ProxtHandler( {} )
        if enable_proxy:
            opener = urllib2.build_opener( proxy_handle )
        else:
            opener = urllib2.build_opener( null_proxy_handle )
        urllib2.install_opener( opener )
        content = urllib2.urlopen( url ).read()
        print len( content )

class NoExceptionCookieProcesser( urllib2.HTTPCookieProcessor ):
    def http_error_403( self, req, fp, code, msg, hdrs ):
        return fp

class Test_httplib( object ):

    def __init__( self, url ):
        self.url = url

    def use_httplib( self ):
        HttpCon = httplib.HTTPConnection( self.url )
        i_headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                    "Accept":"text/plain"}
        HttpCon.request( 'Get', '/', headers = i_headers )
        r1 = HttpCon.getresponse()
        print "version:", r1.version
        print "reason:", r1.reason
        print"status:", r1.status
        print"msg:", r1.msg
        print"headers:", r1.getheaders()
        HttpCon.close()
    
if __name__ == "__main__":
    T_urllb = Test_urllib( 'http://www.baidu.com' )
    T_urllb.use_urltriver()
    T_httplib = Test_httplib( 'www.baidu.com' )
    T_httplib.use_httplib()


