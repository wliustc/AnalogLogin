import requests
import time
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from PIL import  Image
from pyquery import PyQuery as pq

class JdLogin():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer':'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        }

    def get_captcha(self,uuid):
        '''
        先用username验证是否需要验证码
        :param uuid:
        :return:
        '''
        verfiy_url = 'https://passport.jd.com/uc/showAuthCode?r=0.20551138503113386&version=2015'
        verfiy_res= self.session.post(verfiy_url,data={
            'loginName':self.username
        },headers=self.headers)
        url = 'https://authcode.jd.com/verify/image?a=1&acid={}&uid={}&yys={}'.format(uuid,uuid,str(int(time.time()*1000)))
        data = self.session.get(url,headers={
            'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
            'Host':'authcode.jd.com',
            'Referer':'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        })
        with open('captcha.png','wb') as f:
            f.write(data.content)
        im = Image.open('captcha.png')
        im.show()
        captchaCode = input('输入验证码')
        return captchaCode
    def get_pwd(self):
        '''
        function getEntryptPwd(pwd){
            var pubKey = $('#pubKey').val();
            if(!pwd || !pubKey || !SysConfig.encryptInfo){
                return pwd;
            }
            var encrypt = new JSEncrypt();
            encrypt.setPublicKey(pubKey);
            return encrypt.encrypt(pwd);
        }
            :param pubkey:
            :return nloginpwd:
            要用 encrypt 先  set  后get 传入
        '''
        pubkey= '''-----BEGIN PUBLIC KEY-----
            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5lalja
            N9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7P
            AzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQ
            q+CA6agNkqly2H4j6wIDAQAB
            -----END PUBLIC KEY-----'''
        rsakey = RSA.importKey(pubkey)
        cipher = PKCS1_v1_5.new(rsakey)
        text = base64.b64encode(cipher.encrypt(self.password.encode()))
        return text.decode()

    def login(self):
        login_url = 'https://passport.jd.com/new/login.aspx'
        login_res = self.session.get(login_url,headers=self.headers)
        uuid = re.findall(' name="uuid" value="(.+)"/>',login_res.text)[0]
        sa_token = re.findall('name="sa_token" value="(.+)"/>',login_res.text)[0]
        pubkey = re.findall('id="pubKey" value="(.+)" class="hide"/',login_res.text)[0]
        captcha_code = self.get_captcha(uuid)

        post_url = 'https://passport.jd.com/uc/loginService?uuid={}&ReturnUrl=https%3A%2F%2Fwww.jd.com%2F&r=0.632371520512887&version=2015'.format(uuid)
        post_data = {
            'uuid':uuid,
            'eid':'S7SPCXJOTNFHL6C237XXM7E2THUJNBTJBXDZCSXBHD2EA46KENWFUCPHWCOPYIXJNVVUDVOLQZOWSK5FYE33GCVVWM',
            'fp':'2cd9c3cb84c9f9536491cff1167d9dd3',
            '_t':'_t',
            'loginType':'c',
            'loginname':self.username,
            'nloginpwd':self.get_pwd(),
            'chkRememberMe':'',
            'authcode':captcha_code,
            'pubKey':pubkey,
            'sa_token':sa_token
        }
        post_res = self.session.post(post_url,data=post_data,headers=self.headers)
        s =  eval("u"+"\'"+post_res.text+"\'")
        if '验证码不正确' in s:
            print('验证码错误')
            self.login()
        elif '账户名与密码不匹配' in s:
            print('账户名与密码不匹配，请重新输入')

        elif 'success' in s:
            home_page = 'https://home.jd.com/'
            home_res = self.session.get(home_page,headers=self.headers)
            user= re.findall('<a href="//me.jd.com" target="_blank">(.+)</a>',home_res.text)[0]
            print('登录成功 用户名：%s' % user)
            #输出用户名即为成功

if __name__ == '__main__':
    username = input('输入用户名：')
    password = input('输入密码：')
    login = JdLogin(username,password)
    login.login()