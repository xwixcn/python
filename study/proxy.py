#-*-coding:utf-8
'''
用来测试代理访问
'''
import urllib2
def use_proxy():
    enable_proxy = True
    proxy_Handle = urllib2.ProxyHandler( {"http": "http://172.20.23.205:80"} )
    Null_proxy_Handle = urllib2.ProxyHandler( {} )
    if enable_proxy:
        opener = urllib2.build_opener( proxy_Handle )
    else:
        opener = urllib2.build_opener( Null_proxy_Handle )
    urllib2.install_opener( opener )
    try:
        f = urllib2.urlopen( "http://192.168.23.43:8888/search?q=pufayinhang&ti\
                d=spell&spt=1" ).read()
        print f
    except urllib2.HTTPError, e:
        print "HTTPERROR:", e.reason
    except urllib2.URLError, e:
        print "URLERROR:", e.reason
    except Exception, e:
        print e
use_proxy()
