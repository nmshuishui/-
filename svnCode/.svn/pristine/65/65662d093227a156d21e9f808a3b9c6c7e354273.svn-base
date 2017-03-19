# encoding:utf-8
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import traceback

celery = Celery('tasks', broker='amqp://guest@localhost')

# send mail
# authentication failed   认证失败
# smtp.login(username, password) 用户名，密码不正确 或者 mail未开启IMAP POP3等协议
# 为了避免密码泄露造成邮箱安全隐患，需设置客户端授权码，用授权码代替密码在客户端登录邮箱（126邮箱）

mailto_list = ['yongwei.zhang@cloudacc-inc.com']
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "nmgshuishui"  # 用户名
mail_pass = "nmshuishui888"  # 口令,授权码
mail_postfix = "126.com"  # 发件箱的后缀


@celery.task
def send_mail(to_list, sub, content):
    sender = "兵魂后台" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = sender
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        traceback.print_exc(e)
        return False


if __name__ == '__main__':
    send_mail(mailto_list, "what is this?", "hello world！")