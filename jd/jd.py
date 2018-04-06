import requests
import time
import re
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
from PIL import  Image
from pyquery import PyQuery as pq
import random
import os
from http import cookiejar
class JdLogin():
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer':'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        }
        self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
    def load_cookies(self):
        try:
            self.session.cookies.load(ignore_discard=True)
            home_page = 'https://home.jd.com/'
            home_res = self.session.get(home_page, headers=self.headers)
            user = re.findall('<a href="//me.jd.com" target="_blank">(.+)</a>', home_res.text)[0]
            print('登录成功 用户名：%s' % user)
            self.session.cookies.save()
            return True
        except Exception as e:
            print('Cookies.txt 未找到，读取失败')
            return False
    def get_captcha(self,uuid):
        '''
        先用username验证是否需要验证码
        :param uuid:验证码对应的值
        :return:返回是别的验证码
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
        os.remove('captcha.png')

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
            :return nloginpwd:str 加密后的密码
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
        '''
        使用self.get_pwd()获取加密后的密码
        利用验证码, pubkey, token伪造post请求获取登录结果
        :return: 是否登录成功
        '''
        if self.load_cookies():
            return True
        username = input('输入用户名：')
        password = input('输入密码：')
        self.username=username
        self.password=password
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
            self.session.cookies.save(ignore_discard=True, ignore_expires=True)
            s = input('是否购买,购买输入1,否则随意键退出')
            if s == '1':
                id = input('输入商品链接')
                pid = re.findall('\d+', id)[0]
                self.login.add_to_cart(pid)
                self.login.buy_id(pid)
            #输出用户名即为成功
    def get_time(self):
        return str(int(time.time()*1000))
    def  add_to_cart(self,id):
        '''
        根据商品id 讲商品加入购物车
        :param id: 商品识别码
        :return:
        '''
        url4 = 'https://cart.jd.com/gate.action?rd=0.39726436210775695&f=3&pid={}&ptype=1&pcount=1&callback=jQuery8061798&_={}'.format(id,self.get_time())
        res4 = self.session.get(url4,headers=self.headers)
        print(res4.text)


    def get_cart(self):
        '''
        获取购物车内商品
        :return:
        '''
        url = 'https://cart.jd.com/cart?rd%s' % time.time()
        res = self.session.get(url,headers= self.headers)
        html = pq(res.text)
        name = html('div.p-name').text()
        print('name %s' % name)
    def buy_id(self):
        '''
        通过商品的id伪造提交购买订单
        :param pid:
        :return:
        '''
        # 'https://gia.jd.com/y.html?v=0.9520271196999908&o=trade.jd.com/shopping/order/getOrderInfo.action'
        # var jd_risk_token_id='EFNCB57W4CDXKH43EAZEIIQNG7LQY72TWNVNQIC7IIOQFCIHDXJ2FBP32S5GS47LRJIGORFWMF5NW';var pin='FIACATPODPVANT2JNZEK6AC63Y';'
        url = 'https://trade.jd.com/shopping/order/getOrderInfo.action?rid={}'.format(self.get_time())
        res = self.session.get(url,headers=self.headers)
        riskControl  = re.findall('id="riskControl" value="(.+)"/>',res.text)[0]
        post = 'https://trade.jd.com/shopping/order/submitOrder.action'
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        riskControl = 'D0E404CB705B97325B3FD5B6613C678F93893C507A9457906A0F57D52B4C67F5'
        post_data = {
            'overseaPurchaseCookies':'',
            'submitOrderParam.sopNotPutInvoice':'false',
            'submitOrderParam.trackID': cookies.get('TrackId'),
            'submitOrderParam.ignorePriceChange':0,
            'submitOrderParam.btSupport':0,
            'submitOrderParam.eid':'NV4NBKH5AQIV532ZMF7FAQCDYXEC3ZCPXSA5LNXXDUFWMW5DY67MWH4NZPHEE3EKTGI7DU4K47GMPZGZHY354765UE',
            'submitOrderParam.fp':'29ad958ce85dc0137cb1fdabe2522d78',
            'riskControl':riskControl
        }
        post_res  = self.session.post(post,data=post_data,headers=self.headers)
        if ',"resultCode":0,' in post_res.text:
            print('提交购买成功 请登录账号付款')
if __name__ == '__main__':

    login = JdLogin()
    login.login()
