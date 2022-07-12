# -*- coding: utf-8 -*-
import requests
import json
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

temperature = random.randrange(360, 371) / 10.0  # 随机体温
signtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 生成当前时间

#####################    此处设置脚本相关配置    #####################################
##################################################################################

password = ''       # 校园网密码
username = ''       # 校园网账号
grant_type = 'password'
mail_host = ""      # 设置服务器 qq邮箱默认为smtp.qq.com
mail_user = ""      # 用户名
mail_pass = ""      # 口令
toUser = ''         # 邮件接收方姓名
toUserMail = ''     # 邮件接受方邮件地址
data = {"temperature": str(temperature), "isHealth": 1, "isCough": 0, "isFatigue": 0, "isFever": 0, "atDomestic": 0,
        "isCloseContact": 0, "isHomeDiagnosis": 0, "signTime": str(signtime), "code": "",
        "locateAccuracy": "29.374241",  # 纬度
        "locateLatitude": "106.19178",  # 经度
        "locateAccurate": "38.0", "signExcept": 0,
        "detailedAddress": "重庆市--沙坪坝区",
        "locateDetailedAddress": "重庆市电子工程职业学院学生公寓12栋",
        "signType": 1,
        "province": "重庆市", "city": "",
        "county": "沙坪坝区"}   # 这个数据不保证真实性

##################################################################################
##################################################################################

headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; ANA-AN00 Build/HUAWEIANA-AN00; wv) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 MMWEBID/2819 '
                      'MicroMessenger/8.0.19.2080(0x28001339) Process/toolsmp WeChat/arm64 Weixin NetType/4G '
                      'Language/zh_CN ABI/arm64',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '466',
        'Content-Type': 'application/json',
        'Host': 'ossc.cqcet.edu.cn',
        'Origin': 'http://weixin.cqcet.edu.cn',
        'X-Requested-With': 'com.tencent.mm',
    }
session = requests.session()

def sign_main():
    params = (
        ('loginName', username),
        ('access_token', get_token()),
    )

    response = session.post('http://ossc.cqcet.edu.cn/openapi/api-prevention/signinfo/save', headers=headers,
                             params=params, data=json.dumps(data))
    d = json.loads(response.content.decode())
    print(d)
    if d['code'] != 1:
        send_email(d['msg'])


def send_email(msg):
    receivers = [toUserMail]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("服务器", 'utf-8')  # 此处可设置为任意
    message['To'] = Header(toUser, 'utf-8')

    subject = '微信打卡消息:' + msg
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    try:
        # smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    finally:
        smtpObj.quit()

def get_token():
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.108 Safari/537.36'}
    token_params = {'username': username,
                    'password': password,
                    'grant_type': grant_type,
                    'userCode': '',
                    'dataScope': ''}
    url_token = 'http://ossc.cqcet.edu.cn/prevented/v1/token/getToken'
    a = session.get(url=url_token, headers=headers, params=token_params)
    b = json.loads(a.content.decode())
    print('获取token成功：',b)
    return b['access_token']


if __name__ == '__main__':
    sign_main()