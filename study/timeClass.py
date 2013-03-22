#-*-coding:utf-8
#!/usr/bin/python
import datetime
import time
import calendar
def produce_timstamp():
    '''
    产生9位时间戳
    '''
    nowTime = datetime.datetime.now()
    timestamp = int( time.mktime( nowTime.timetuple() ) )
    return timestamp

def lastmonth_Count():
    '''
    统计上个月的天数
    '''
    nowTime = datetime.datetime.now()
    if nowTime.month == 1:
        lastmonth = 12
    else:
        lastmonth = nowTime.month - 1
    return calendar.monthrange( nowTime.year, lastmonth )[1]


def
if __name__ == '__main__':
    atime="2013/02/26"
    nowTime = datetime.datetime.now()


    print nowTime