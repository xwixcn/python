#-*-coding:utf-8
import ConfigParser
import os
import sys

PWD = os.path.dirname( os.path.realpath( __file__ ) )

def load_config( path ):
    config = ConfigParser.RawConfigParser()
    cfg_path = os.path.join( PWD, '%s' % ( path ) )
    try:
        config.read( cfg_path )
    except ConfigParser , error:
        print 'No Such cfg'
        sys.exit( 1 )
    return config




