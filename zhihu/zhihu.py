import requests
import hashlib
import time
import hmac
import re

class ZhihuLogin():
    def __init__(self,username,password):
        #初始化用户名 密码 session  headers
        self.session = requests.session()
        self.username = username
        self.password = password
        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }

    def _get_signurate(self,timestamp):
        #获取加密签名
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        hm.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return hm.hexdigest()
    def get_time(self):
        #获取时间戳
        return str(int(time.time() * 1000))


    def get_captcha(self):
        self.headers.update({
            # 更新headers
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            # 身份认证信息
            'X-Xsrftoken': self.session.cookies.get('_xsrf'),
        })
        captchaurl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        res = self.session.get(captchaurl, headers=self.headers)
        if 'True' in res.text:
            print('请输入验证码')
            pass
        else:
            print('')
    def login(self):
        self.get_captcha()
        #构造postdata
        post_data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp': self.get_time(),
            'source': 'com.zhihu.web',
            'signature': self._get_signurate(self.get_time()),
            'username': '+8615101528779',
            'password': 'aq918927',
            'captcha': '',
            'lang': 'cn',
            'ref_source': 'homepage',
            'utm_source': '',
        }
        loginUrl = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        res = self.session.post(loginUrl, data=post_data, headers=self.headers)
        auth = re.findall('"z_c0":"(.+)"},"refresh_token"',res.text)[0]
        self.headers.update({'authorization':auth})
        ifLogin = self.session.get('https://www.zhihu.com/api/v4/me?include=visits_count',headers=self.headers).json()
        if ifLogin.get('name'):
            print('登录成功 用户名为：%s' % ifLogin.get('name'))
    def send(self,message):
        post_data = {
            "type": "common",
            "content": message,
            "receiver_hash": "c1bec6c58a14d9e4265f2dddcf59308d"
        }
        sendUrl = 'https://www.zhihu.com/api/v4/messages'
        res = self.session.post(sendUrl,data=post_data,headers=self.headers)
        print(res.text)



if __name__ == '__main__':
    username = input('输入用户名：')
    password = input('输入密码：')
    login = ZhihuLogin(username,password)
    login.login()


