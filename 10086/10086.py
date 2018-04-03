import requests
import time
import random
import urllib.parse
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from PIL import Image

class yidongLogin():
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.headers= headers = {
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
				'Host':'login.10086.cn',
				'Referer':'https://login.10086.cn/html/window/loginMini.html?channelID=12003&backUrl=http://shop.10086.cn/i/sso.html'
		}
		#持久化session
		self.session = requests.session()

	def get_login_captcha(self):
        #发送短信验证码
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
			print('发送失败')
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

	def get_login_info(self):
		self.get_login_captcha()
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
		cookies = {
			'CmLocation': '100|100',
			'CmProvid': 'bj',
			'ssologinprovince': '100'
		}
		print(artifactUrl)
		self.session.get(artifactUrl, headers=self.headers, cookies=cookies)

		infourl = 'http://shop.10086.cn/i/v1/cust/info/' + self.username + '?_=' + str(int(time.time() * 1000))
		infores = self.session.get(infourl, headers=self.headers, cookies=cookies)
		print('gerenxinxi %s ' % infores.text)


if __name__ == '__main__':
    username = input('输入用户名：')
    password = input('输入密码：')
    login = yidongLogin(username,password)
    login.get_login_info()