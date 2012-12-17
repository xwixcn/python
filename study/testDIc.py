#-*-coding:utf-8
from  multiprocessing import process
import threading


class test_thread():
    '''
    测试多线程
    '''
    def __init__(self):
        pass

    def foo(self,begin,end):
        x=begin
        while x<end:
            print x
            x=x+1

    def thread(self):
        th=threading.Thread(target=self.foo(4,5))
        th.daemon=True
        th.start()
        th.join()


class test_process(process.Process):
    '''
    测试多进程
    '''
    def run(self):
        print 'test',self.name

    def start(self):
        self.run()
    

if __name__=="__main__":
    a=test_process()
    a.start()

