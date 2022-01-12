import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '18901671371@163.com'  # 发件人邮箱账号
my_pass = 'CJUPDICSNUIOIMYV'  # 发件人邮箱密码
# my_user = '714420577@qq.com'  # 收件人邮箱账号，我这边发送给自己

def mailCn(reveiver, cn):
    ret = True
    try:
        msg = MIMEText(f"Votre code secret de vote est:{cn},\nNe parlez à personne de votre code,s'il vous plaît", 'plain', 'utf-8')
        msg['From'] = formataddr(["Vote System 1.0", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Voter", reveiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Votre code secret de vote"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [reveiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

def mailVeri(reveiver, rand):
    ret = True
    try:
        msg = MIMEText(f"Votre code de vérification est:{rand},\nNe parlez à personne de votre code,s'il vous plaît", 'plain', 'utf-8')
        msg['From'] = formataddr(["Vote System 1.0", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["Voter", reveiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Votre code de vérification"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [reveiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
