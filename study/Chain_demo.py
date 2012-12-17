#-*-coding:utf-8
#!/usr/bin/python
#author:lhb
#Createtime:2012/8/15

class Abstarct_Print():
    
    def __init__( self ):
        pass

    def  print_OK( self ):
        pass

    def print_Sorry( self ):
        pass

class Print_OK( Abstarct_Print ):

    def __init__( self ):
        Abstarct_Print.__init__( self )

    def print_OK( self ):
        print 'OK'


if __name__ == "__main__":
    a = Print_OK()
    a.print_OK()

