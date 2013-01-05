#!/usr/bin/env python
# -*- coding=utf-8 -*-

import web
import model
import json

urls = ( 

         '/home', 'index',
         
         '/tag', 'tagindex',
         '/tag/get', 'tagget',
         '/tag/edit/(\d+)', 'tagedit',
         
         '/config/show', 'readconfig',
         '/config/edit', 'editconfig',
         
         '/case/(\d+)', 'caseget',
         '/case/edit/(\d+)', 'caseedit',
         
         '/result', 'resultindex',
         '/result/round/(\d+)', 'getroundIDdata',
         '/result/type/(.*)', 'getTypedata',
         
         '/job', 'jobindex',
         '/job/start/(.*)', 'jobstart',
         '/job/kill/(\d+)', 'jobkill',
         '/job/status/(\d+)', 'jobstatus',
         '/job/record/(\d+)', 'jobrecord'
 
     )

render = web.template.render( 'templates' )
jobrender = web.template.render( 'templates/job' )
caserender = web.template.render( 'templates/tag' )
resultrender = web.template.render( 'templates/result' )
#result zone
app = web.application( urls, globals() )


class index:
    def GET( self ):
        return render.index()
    def POST( self ):
        data = web.data()
        return data

class resultindex:
    '''
    show the home page
    '''
    def GET( self ):    
        ( status, data ) = model.getAllData() 
        if status == 0:
            return resultrender.resultmanager( data )
        else:
            return web.notfound()
    
        
class getroundIDdata:
    '''
    show  each round of the webpage 
    '''
    def GET( self, num ):
        ( status, data ) = model.getroundIDdata( num )
        if status == 0:
            return resultrender.roundIDdata( num, data )
        else:
            return web.notfound( data )

class getTypedata:
    '''
    Different types of data
    '''
    def GET( self, Type ):
        ( status, data ) = model.gettypedata( Type )
        if status == 0:
            return resultrender.sourcetype( Type, data )
        else:
            return web.notfound( data )

 
class readconfig:
    '''
    show the edit config page
    '''
    def GET( self ):
        data = model.getconfigcontent()
        print data
        return render.config( data )

class editconfig:
    '''
    write the configcontent
    '''
    def POST( self ):
        data = web.data()
        model.setconfigcontent( data )
        return "配置文件修改成功"


#result zone    

#case zone
class caseget:
    '''
    tag首页
    '''
    def GET( self, tag ):
        data = model.getcase( tag )
        return data


class caseedit:
    '''
    编辑case
    '''
    def POST( self , tagid ):
        data = web.data()
        status = model.postcase( tagid, data )
        return status

#tag zone
class tagindex:
    def GET( self ):
        return caserender.tag()
    
class tagget:
    def GET( self ):
        data = model.gettagcontent()
        print data
        return data

class tagedit:
    '''
    编辑tag
    '''
    def POST( self , tagid ):
        data = web.data()
        print data
        status = model.posttag( tagid, data )
        return status
#job zone
class jobindex:
    '''
    job首页
    '''
    def GET( self ):
        return jobrender.jobcontrol()

class jobstart:
    '''
    启动一个job
    '''
    def GET( self, jobname ):
        data = model.startjob( jobname )
        return data

class jobstatus:
    '''
    获取一个job状态
    '''
    def GET( self , jobid ):
        data = model.getstatus( jobid )
        return data


class jobkill:
    '''
    停止job
    '''  
    def GET( self, jobid ):
        data = model.killjob( jobid )
        return data
class jobrecord:
    '''
    返回job的运行记录页面
    '''
    def GET( self , num ):
        return jobrender.jobrecord()

#application = app.wsgifunc()
if __name__ == "__main__":
    app = web.application( urls, globals() )
    app.run()


