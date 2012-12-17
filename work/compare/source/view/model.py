#-*-coding:utf-8
import web, datetime
from code.MainCompare import *
import urllib2
import json
from code.config_agent import *
import sys
import urllib
import ConfigParser
sys.path.append( "code/compare.cfg" )

'''proxy_Handle = urllib2.ProxyHandler( {"http": "http://172.20.23.205:80"} )
opener = urllib2.build_opener( proxy_Handle )
urllib2.install_opener( opener )
'''
def urldecode( query ):
    '''
    decode the param
    '''
    d = {}
    a = query.split( '&' )
    value = []
    result = []
    for s in a:
        if s.find( '=' ):
            k, v = map( urllib.unquote, s.split( '=' ) )
            value.append( v )
    result = [value[i:i + 2] for i in range( 0, len( value ) - 1, 2 )]
    return result


def postsitedata():
    '''
    发送单个网站数据
    '''
    main = MainCompare()
    main.postData( 0 )
    
def postcomparedata():
    '''
    发送网站比对结果
    '''
    main = MainCompare()
    main.postData( 1 )

def getAllData():
    '''
    获取要展示的web数据
    '''
    config = load_config( "compare.cfg" )
    alldataurl = config.get( '前台展示', '所有结果地址' )
    try:
        data = urllib2.urlopen( alldataurl ).read()
        data = json.loads( data )
        return 0, data
    except Exception, e:
        return 1, str( e )

def getroundIDdata( i ):
    config = load_config( "compare.cfg" )
    roundidurl = config.get( '前台展示', '每轮结果地址' )
    try:
        data = urllib2.urlopen( roundidurl + "%s" % ( i ) ).read()
        data = json.loads( data )["result"]
        return 0, data
    except Exception, e:
        return 1, str( e )

def gettypedata( Type ):
    config = load_config( "compare.cfg" )
    roundidurl = config.get( '前台展示', '每轮结果地址' )
    try:
        data = urllib2.urlopen( roundidurl + '%s' % ( Type ) ).read()
        data = json.loads( data )
        return 0, data
    except Exception, e:
        return 1, str( e )
    
def getconfigcontent():
    config = load_config( "compare.cfg" )
    sections = config.sections()
    sectiondic = {}
    for section in sections:
        sectiondic[section] = config.items( section )
    print sectiondic
    return sectiondic

def setconfigcontent( data ):
    config = load_config( "compare.cfg" )
    sections = config.sections()
    sectionlist = [len( config.items( section ) ) for section in sections]
    i = 0
    splitlist = []
    for x in sectionlist:
        splitlist.append( ( i, i + x ) )
        i = i + x
    result = urldecode( data )
    sectionlist = [result[a:b]for a, b in splitlist]
    i = [len( a )for a in sectionlist]
    for content, section in zip( sectionlist, config.sections() ):
        for elem in content:
            config.set( section, elem[0], elem[1] )
    config.write( open( 'code/compare.cfg', 'wb' ) )

def getselectdata():
    
    return urllib2.urlopen( "http://192.168.23.75/backend/casemanager/regression" ).read()

def gettagcontent( i ):
    return urllib2.urlopen( "http://192.168.23.75/backend/casemanager/tag/%s" % ( i ) ).read()

def postData( url, resultdata ):
    headers = {"Accept":"application/json", "Content-Type":"application/x-www-form-urlencoded"}
    req = urllib2.Request( url = url, data = "%s" % ( resultdata ), headers = headers )
    urllib2.urlopen( req ).read()
        
if __name__ == "__main__":
    #setconfigcontent('fname=%E6%8E%A5%E6%94%B6%E9%97%AE%E5%8F%A5%E5%9C%B0%E5%9D%80&lname=http%3A%2F%2F192.168.23.75%2Fbackend%2Fcases%2Fmonitor%2Fmin&fname=%E5%8F%91%E9%80%81%E7%BB%93%E6%9E%9C%E5%9C%B0%E5%9D%80&lname=http%3A%2F%2F192.168.23.75%2Fbackend%2Fresults%2Fverify%2F&fname=%E8%BF%9B%E7%A8%8B%E6%95%B0&lname=10&fname=%E6%B5%8B%E8%AF%95%E7%8E%AF%E5%A2%83&lname=http%3A%2F%2F192.168.23.105&fname=%E5%9F%BA%E5%87%86%E7%8E%AF%E5%A2%83&lname=http%3A%2F%2F192.168.23.105&fname=%E6%89%80%E6%9C%89%E7%BB%93%E6%9E%9C%E5%9C%B0%E5%9D%80&lname=http%3A%2F%2F192.168.23.75%2Fbackend%2Fresults%2Fall&fname=%E6%AF%8F%E8%BD%AE%E7%BB%93%E6%9E%9C%E5%9C%B0%E5%9D%80&lname=http%3A%2F%2F192.168.23.75%2Fbackend%2Fresults%2F&fname=%E6%B5%8B%E8%AF%95%E7%8E%AF%E5%A2%83&lname=http%3A%2F%2F192.168.23.105')
   pass 
