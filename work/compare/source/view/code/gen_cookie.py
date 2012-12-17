# -*- coding: utf-8 -*-

import cookielib
import urllib2

def gen_cookie(url ):
    filename=url.lstrip("http://")
    cj = cookielib.LWPCookieJar( filename )
    cjhandler = urllib2.HTTPCookieProcessor( cj )
    opener = urllib2.build_opener( cjhandler )
    urllib2.install_opener( opener )
    openurl=url+'/stockpick/search?tid=stockpick&w=%E7%AB%9960%E6%97%A5%E5%9D%87%E7%BA%BF%E4%B8%8A&source=data'
    resp = urllib2.urlopen( openurl )
    cj.save()
    resp.read()

if __name__=="__main__":
    gen_cookie("http://192.168.23.105")


