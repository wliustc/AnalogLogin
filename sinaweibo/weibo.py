import requests
import time
import rsa
import re
import binascii
import json
import urllib
import base64
class Launcher():
    def __init__(self,username,password):
        #初始化 用户名 密码 session headers
        self.username = username
        self.password = password
        self.session =  requests.session()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
    def pubkeyData(self):
        #获取 pubkey 数据
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=pluginSSOController.preloginCallBack&su=MTUxMDE1Mjg3Nzk%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_='+str(int(time.time()*1000))
        req = self.session.get(url,headers=self.headers)
        data = json.loads(re.findall('preloginCallBack\(({.+})',req.text)[0])
        return data

    def get_pwd(self, data):
        #加密密码
        rsa_e = int('10001',16)
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 安全起见清空明文密码
        passwd = binascii.b2a_hex(pw_encypted)
        return passwd

    def get_su(self):
        username_urllike = urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike, encoding='utf-8'))
        return username_encrypted.decode('utf-8')  # 将bytes对象转为str
    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        data = self.pubkeyData()
        #构造 post数据 
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "qrcode_flag":'false',
            "useticket": "1",
            "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
            "vsnf": "1",
            "su": self.get_su(),
            "service": "miniblog",
            "servertime": data['servertime'],
            "nonce": data['nonce'],
            "pwencode": "rsa2",
            "rsakv": data['rsakv'],
            "sp": self.get_pwd(data),
            "sr": "1920*1080",
            "encoding": "UTF-8",
            "prelt": "194",
            "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }

        res = self.session.post(url,data=post_data,headers=self.headers)
        # print(res.text)
        #post 后会返回 重定向页面的网址
        url2 = re.findall('location\.replace\("(https://.+)"\);',res.content.decode('gbk'))[0]
        res2 = self.session.get(url2,headers=self.headers)
        url3 = re.findall("location\.replace\('(https://.+)'\);",res2.content.decode('gbk'))[0]
        res3 = self.session.get(url3,headers=self.headers)
        #重定向结束后 登录成功 访问你的首页 通过判断你的用户名是否存在来认定是否登录成功
        loginurl = 'http://weibo.com'+re.findall('"userdomain":"(.+)}}',res3.text)[0]
        loginres = self.session.get(loginurl,headers=self.headers).text
        try:
            username = re.findall(r"\$CONFIG\['nick'\]='(.+); ", loginres)[0]
        except Exception as e:
            print(e)
        if username:
            print('登录成功 当前用户为；%s' % username)


if __name__ == '__main__':
    s = Launcher('15101528779','aq918927')
    s.login()