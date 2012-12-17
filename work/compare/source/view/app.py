#!/usr/bin/env python
# -*- coding=utf-8 -*-

import web
import model
import json



#from compare import Compare

urls = ( 

         '/home', 'index',
         '/rounddata/(\d+)', 'getroundIDdata',
         '/results/(.*)', 'getTypedata',
         '/start/single', 'singlecompare',
         '/start/multi', 'multicompare',
         '/to/control', 'jumptocontrol',
         '/get/config', 'readconfig',
         '/edit/config', 'editconfig',
         '/casemanager', 'casemanage',
         '/casemanager/regression', 'getselectdata',
         '/casemanager/tag/(\d+)', 'gettagcontent'
 
         

     )

render = web.template.render( 'templates' )

class index:
    '''
    show the home page
    '''
    def GET( self ):    
        ( status, data ) = model.getAllData() 
        if status == 0:
            return render.index( data )
        else:
            return web.notfound()
        
class getroundIDdata:
    '''
    show  each round of the webpage 
    '''
    def GET( self, num ):
        ( status, data ) = model.getroundIDdata( num )
        if status == 0:
            return render.roundIDdata( num, data )
        else:
            return web.notfound( data )

class getTypedata:
    '''
    Different types of data
    '''
    def GET( self, Type ):
        ( status, data ) = model.gettypedata( Type )
        if status == 0:
            return render.sourcetype( Type, data )
        else:
            return web.notfound( data )

class jumptocontrol:
    '''
    jump to the control page
    '''
    def GET( self ):
        return render.control()
      
class multicompare:
    '''
    exec the multicompare task
    '''
    def GET( self ):
        model.postcomparedata()
        return 'OK'

class singlecompare:
    '''
    exec the singlesitedata task
    '''
    def GET( self ):
        model.postsitedata()
        return 'OK'
        #web.seeother( '/home' )
        
class readconfig:
    '''
    show the edit config page
    '''
    def GET( self ):
        data = model.getconfigcontent()
        print data
        return render.config( data )
    def POST( self ):
        data = web.data()
        model.setconfigcontent( data )
        web.seeother( '/get/config' )

class editconfig:
    '''
    write the configcontent
    '''
    def POST( self ):
        data = web.data()
        model.setconfigcontent( data )
        return "配置文件修改成功"

class casemanage:
    '''
    show the casemanager page
    '''
    def GET( self ):
        return render.content()
    def POST( self ):
        data = web.data()
        print data
        return "删除成功"

class gettagcontent:
    '''
    get each tag data
    '''
    def GET( self, i ):
        data = model.gettagcontent( i )
        return data
    
class getselectdata:
    '''
    get the select data
    '''
    def GET( self ):
        data = model.getselectdata()
        return data;

app = web.application( urls, globals() )
application = app.wsgifunc()
#if __name__ == "__main__":
#    app = web.application( urls, globals() )
#    app.run()


