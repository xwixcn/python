import os

def testfork():
    pid1=os.fork()
    print pid1
    pid2=os.fork()
    print pid2
    print 'pid1:%s\tpid2:%s'%(pid1,pid2)


if __name__=="__main__":
    testfork()


