#! /usr/bin/env python
import Httpsqs
import json
import socket
import time

queuenames =['logQueue']
hq3=Httpsqs('192.168.23.207',port=1218)
def get_info():
    for queuename in queuenames:
        st1 = json.loads(hq3.status_json(queuename))
        f1 = open('./data/3_'+queuename,'w')
        for i in range(0,40000):

            try:
                data = hq3.get_read_info(queuename,i)
                f1.write(data + '\n')
            except socket.error,e:
                pass
                time.sleep(5)
        f1.close()

def put_info():
    for queuename in queuenames:
        f1 = open('./data/93_'+queuename)
        f2 = open('./data/94_'+ queuename)
        for li in f1.read().split('\n'):
            try:
                hq1.put(queuename,li)
            except socket.error:
                print "hq1 encounter error"
                time.sleep(10)
        for li in f2.read().split('\n'):
            try:
                hq2.put(queuename,li)
            except socket.error:
                print "hq2 encounter error"
                time.sleep(10)
    
        print "put data to queue done"
        print hq1.status_json(queuename)
        print hq2.status_json(queuename)
    print "all done"

def get_status():
        st3 = json.loads(hq3.status_json("crawler_queue_inte_test_2"))
        print "23.207 \t",st3


if __name__ == '__main__':
    #put_info()
    try:
        get_info()
    except Exception,e:
        if 'Connection refused'in  str(e):
            print 'eeeee'

