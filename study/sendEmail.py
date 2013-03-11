#-*-coding:utf-8
#!/usr/bin/python
#
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen

#从文件读
file_ob = open( '/home/mailcontent.txt' )
try:
    content = file_ob.read()
finally:
 	file_ob.close()
msg = MIMEText( content, 'plain', 'utf-8' )
msg['Subject'] = 'this is a test from python'
msg['From'] = 'from@163.com'
msg['To'] = 'to@qq.com'

#从网页读
f = urlopen( 'http://www.pcesen.com' )
msg = MIMEText( f.read(), 'html', 'utf-8' )
msg['Subject'] = 'this is a test from python'
msg['From'] = 'from@163.com'
msg['To'] = 'to@qq.com'
msg['Cc'] = mail_cc


smtp = smtplib.SMTP()
#协议
smtp.connect( "smtp.163.com", "25" )
#登陆
smtp.login( 'from', 'password' )
smtp.sendmail( 'from@163.com', 'to@qq.com', msg.as_string() )
smtp.quit()
