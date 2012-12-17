# -*- coding: utf-8 -*-
import urllib2
import json
from regressLogger import * 
import cookielib
import sys
import socket
from gen_cookie import *
from distutils.log import Log
log=create_log("webdatautil")
class webdataUtil:
    def __init__( self, cookiefile ):
        cj = cookielib.LWPCookieJar()
        cj.revert( cookiefile )
        cjhandler = urllib2.HTTPCookieProcessor( cj )
        self.opener = urllib2.build_opener( cjhandler )
        #urllib2.install_opener(opener)

    def __getopenhandle( self , cookiefile ):
        cj = cookielib.LWPCookieJar()
        cj.revert( cookiefile )
        cjhandler = urllib2.HTTPCookieProcessor( cj )
        
    def __testcookie( self ):
        try:
            #data = urllib2.urlopen(query).read()
            data = self.opener.open( query ).read()
            return 0, data
        except ( IOError, urllib2.HTTPError, urllib2.URLError ), e:
            if "Connection refused" in str( e ):
                return -1
        return 1
    def __struct_dict( self, dic ):
        rlt = {}
        titlelist = dic.get( 'title' )
        #title_opt = [self.__strip_title(title) for title in titlelist]
        #rlt['title'] = title_opt
        #print dic.get('result')
        try:
            for key, result in dic.get( 'result' ).items():
                stockcode = self.__strip_stockcode( key )
                tmp = {}
                for counter, item in enumerate( result ):
                    tmp[self.__strip_title( titlelist[counter] )] = item
                rlt[stockcode] = tmp
        except AttributeError, e:
            print e.message
            print'对不起，该query没有问答数据'
        return rlt

    def __strip_title( self, title ):
        return title.split( '<' )[0].strip()


    def __strip_stockcode( self, stockcode ):
        return stockcode.split( '.' )[0]


    def __struct_url( self, url, sentence ):
        if url.endswith( '/' ):
            return url + 'stockpick/search?w=' + urllib2.quote( sentence ) + "&source=data"
        else:
            return url + '/stockpick/search?w=' + urllib2.quote( sentence ) + "&source=data"

    def get_ontology_data( self, url, sentence ):
        query = self.__struct_url( url, sentence )
        data = ""
        try:
            #data = urllib2.urlopen(query).read()
            data = self.opener.open( query ).read()
            #print data
        except ( IOError, urllib2.HTTPError, urllib2.URLError ), e:
            log.error( e )
        returndata = ""
        try:
            returndata = json.loads( data )
        except ValueError, UnboundLocalError:
            log.debug( sentence.decode( 'utf-8' ) + "not return json data" )
        return returndata



    def struct_web_data( self, dic, rdclient ):
        """
        dic struct is:
            {stockcode:{title:value}}
        """
        dic_opt = {}
        for stockcode, item in dic.items():
            tmp = {}
            for title, value in item.items():
                #decode data get from redis as redis encoding is different
                title_opt = rdclient.get( title ).decode( 'utf-8' ) if rdclient.get( title ) else title
                tmp[title_opt] = value
            dic_opt[stockcode] = tmp
        return dic_opt

    def restruct_data( self, li ):
        """restruct data from list
        to dict"""
        dic = {}
        for l in li:
            dic[l[0]] = l[1]
        return dic

if __name__ == '__main__':
    wd = webdataUtil( '192.168.23.105' )
    query ="2012中报净利润(同比增长大增长率>100%以上的股票"
    print wd.get_ontology_data( 'http://192.168.23.105', query )
