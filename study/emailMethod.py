#-*-coding:utf-8
#!/usr/bin/python
#
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen


file_ob = open( '/home/mailcontent.txt' )
try:
    content = file_ob.read()
finally:
 	file_ob.close()
msg = MIMEText( content, 'plain', 'utf-8' )
msg['Subject'] = 'this is a test from python'
msg['From'] = 'from@163.com'
msg['To'] = 'to@qq.com'


f = urlopen( 'http://www.pcesen.com' )
msg = MIMEText( f.read(), 'html', 'utf-8' )
msg['Subject'] = 'this is a test from python'
msg['From'] = 'from@163.com'
msg['To'] = 'to@qq.com'
msg['Cc'] = mail_cc


smtp = smtplib.SMTP()

smtp.connect( "smtp.163.com", "25" )

smtp.login( 'from', 'password' )
smtp.sendmail( 'from@163.com', 'to@qq.com', msg.as_string() )
smtp.quit()
