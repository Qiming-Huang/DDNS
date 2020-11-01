from requests_html import HTMLSession
import smtplib
from email.mime.text import MIMEText
import time

current_ip = '49.72.58.66'
mail_host = 'smtp.163.com'
mail_user = '13324811901'
mail_pass = 'ZGHKSEWBQSMUNGBS'

sender = '13324811901@163.com'
receivers = ['727534525@qq.com']
url = 'http://cip.cc'
cot = 0

from requests.exceptions import ConnectionError

def sleep_time(hour, min, sec):
    return hour*3600 + min*60 + sec

wait_time = sleep_time(0,30,0)

while True:
    session = HTMLSession()
    try:
        r = session.get(url)
        about = r.html.find('pre', first=True)
    except ConnectionError:
        print('No Network!!')
        time.sleep(wait_time)
        continue
    try:
        ip_address = about.text.split(' ')[2]
    except AttributeError:
        continue
    if ip_address == current_ip:
        print('ip address did not change! times:' + str(cot))
    else:
        current_ip = ip_address
        message = MIMEText(current_ip, 'plain', 'utf-8')
        message['Subject'] = 'ip address'
        message['From'] = sender
        message['To'] = receivers[0]
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print('successfully send new ip_address, it was:' + current_ip)
        except smtplib.SMTPException as e:
            print('Error')

    cot += 1
    time.sleep(wait_time)