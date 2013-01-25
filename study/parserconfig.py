#-*-coding:utf-8
#config
import ConfigParser
config = ConfigParser.RawConfigParser()
import urldecode
#读取配置文件内容,以dic格式输出
def getconfigcontent( cfg ):
    config.read( cfg )
    sections = config.sections()
    sectiondic = {}
    for section in sections:
        sectiondic[section] = config.items( section )
    return sectiondic

#把http请求解析成
def setconfigcontent( query ):
    config = load_config( "compare.cfg" )
    sections = config.sections()
    sectionlist = [len( config.items( section ) ) for section in sections]
    i = 0
    splitlist = []
    for x in sectionlist:
        splitlist.append( ( i, i + x ) )
        i = i + x
    result = urldecode( query )
    sectionlist = [result[a:b]for a, b in splitlist]
    i = [len( a )for a in sectionlist]
    for content, section in zip( sectionlist, config.sections() ):
        for elem in content:
            config.set( section, elem[0], elem[1] )
    config.write( open( 'code/compare.cfg', 'wb' ) )
