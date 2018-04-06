import requests
import time
import random
import urllib.parse
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from PIL import Image
from http import cookiejar


class yidongLogin():
	def __init__(self,username):
		self.username = username
		self.headers= headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
				'Host':'login.10086.cn',
				'Referer':'https://login.10086.cn/html/window/loginMini.html?channelID=12003&backUrl=http://shop.10086.cn/i/sso.html'
		}
		#持久化session
		self.session = requests.session()
		self.session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
	def get_login_captcha(self):
		'''
		根据用户手机号发送短信验证码
		:return: bool
		'''
		self.session.get('http://shop.10086.cn/i/v1/auth/loginfo?_=' + str(int(time.time() * 1000)), headers=self.headers)
		indexUrl = 'http://shop.10086.cn/i/?f=home'
		res2 = self.session.get(indexUrl, headers=self.headers)
		randomUrl = 'https://login.10086.cn/sendRandomCodeAction.action'
		randomData = {
			'userName': self.username,
			'type': '01',
			'channelID': '12034'
		}
		randomRes = self.session.post(randomUrl, data=randomData, headers=self.headers)
		if randomRes.text == '0':
			print('登录验证码发送成功')
		else:
			print('发送失败，请在一分钟后重试')
	def get_pwd(self):
        #公钥 要用encrpyt转换一下
		pubkey = '''-----BEGIN PUBLIC KEY-----
			MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJF
			mw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9
			zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9Zm
			maFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4eb
			ooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyj
			fey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8Lgbb
			WQIDAQAB
			-----END PUBLIC KEY-----'''
		rsakey = RSA.importKey(pubkey)
		cipher = PKCS1_v1_5.new(rsakey)
		text = base64.b64encode(cipher.encrypt(self.password.encode()))
		return text.decode()
	def check_login(self):
		'''
		根据能否找到用户名来判断登录结果
		:return: bool
		'''
		infourl = 'http://shop.10086.cn/i/v1/cust/info/' + self.username + '?_=' + str(int(time.time() * 1000))
		infores = self.session.get(infourl, headers=self.headers)
		if infores.json()['data']['name']:
			print('登录成功 %s ' % infores.json()['data']['name'])
			filename = 'cookies.txt'
			self.session.cookies.save(ignore_discard=True, ignore_expires=True)
			return True
		else:
			return False
	def load_cookies(self):
		'''
        加载上次保存的cookie文件
        不存在返回False
        :return:  Bool
        '''
		try:
			self.session.cookies.load(ignore_discard=True)
			return True
		except FileNotFoundError:
			print('Cookies.txt 未找到，读取失败')
			return False
	def get_login_info(self):
		'''
		在上一次cookie不存在或失效的情况下重新登陆
		可用直接判断是否登录成功
		:return:
		'''
		if self.load_cookies() and self.check_login():
			return True
		else:
			print('cookie 过期 重新登陆')
			self.password = input('输入密码：')
		self.get_login_captcha() #获取并显示验证码
		smsPwd = input('请输入验证码:')

		loginUrl = 'https://login.10086.cn/login.htm'
		loginData = {
			'accountType': '01',
			'account': self.username,
			'password': self.get_pwd(),
			'pwdType': '01',
			'smsPwd': smsPwd,
			'inputCode': '',
			'backUrl': 'http://shop.10086.cn/i/sso.html',
			'rememberMe': '0',
			'channelID': '12034',
			'protocol': 'https:',
		}

		loginRes = self.session.get(loginUrl, params=loginData, headers=self.headers)
		try:
			artifact = loginRes.json()['artifact']
		except Exception as e:
			print(e)
		artifactUrl = 'http://shop.10086.cn/i/v1/auth/getArtifact?backUrl=http://shop.10086.cn/i/sso.html&artifact={}'.format(
			artifact)
		self.session.get(artifactUrl, headers=self.headers)

		self.check_login()

if __name__ == '__main__':
    username= input('输入账号：')
    login = yidongLogin(username)
    login.get_login_info()