from requests_html import HTMLSession
import smtplib
from email.mime.text import MIMEText
import time

current_ip = 'xxx' # your current ip address
mail_host = 'smtp.xxx.com' # your mail server which support smtp
mail_user = 'xxx'
mail_pass = 'xxxx' # secret key provided by your email server, it's not your email password

sender = 'xxx'
receivers = ['xxx']
url = 'http://cip.cc' # the website could return your public ip address
cot = 0

from requests.exceptions import ConnectionError

def sleep_time(hour, min, sec):
    return hour*3600 + min*60 + sec

wait_time = sleep_time(0,30,0) # define the sleeping time

while True: # get the ip address
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
    else: # if ip address changed, send email
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