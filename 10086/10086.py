import requests
import time
import random
import urllib.parse
import base64
import rsa
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from PIL import Image
from http import cookiejar


class yidongLogin():
	def __init__(self,username, password):
		self.username = username
		self.password = password
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
			artifactUrl = 'http://shop.10086.cn/i/v1/auth/getArtifact?backUrl=http://shop.10086.cn/i/sso.html&artifact={}'.format(
				artifact)
			self.session.get(artifactUrl, headers=self.headers)

			self.check_login()
		except Exception as e:
			print(e)
	def get_randCode(self,code):
		text = base64.b64encode(code.encode())
		return text.decode()
	def get_records(self):
		#发送验证码
		html_url = 'https://shop.10086.cn/i/v1/fee/detbillrandomcodejsonp/{}?callback=jQuery183015845424583577938_1524716409747&_={}'
		html_url = html_url.format(self.username, str(int(time.time()*1000)))
		res = self.session.get(html_url, headers=self.headers )
		print(res.text)
		pwdTempSerCode = input('输入短信随机码：')
		#获取验证码
		capthca_url ='http://shop.10086.cn/i/authImg?t='+str(time.time())
		with open('records.png','wb') as f:
			f.write(self.session.get(capthca_url,headers=self.headers).content)
		im = Image.open('records.png')
		im.show()
		captchaVal = input('输入验证码：')

		#身份认证
		get_url = 'https://shop.10086.cn/i/v1/fee/detailbilltempidentjsonp/{}?callback=jQuery183015845424583577938_1524716409747&pwdTempSerCode={}&pwdTempRandCode={}&captchaVal={}&_={}'
		get_url = get_url.format(self.username, self.get_randCode(self.password), self.get_randCode(pwdTempSerCode), captchaVal, str(int(time.time()*1000)))
		print(get_url)
		res = self.session.get(get_url,headers=self.headers)
		print(res.text)
		#验证 验证码正确
		current_url ='http://shop.10086.cn/i/v1/res/precheck/{}}?captchaVal={}&_=1524716651808'
		#获取通话详单
		records_url ='https://shop.10086.cn/i/v1/fee/detailbillinfojsonp/{}}?callback=jQuery183015845424583577938_1524716409747&curCuror=1&step=100&qryMonth=201802&billType=04&_={}'
		records_url = records_url.format(self.username, str(int(time.time()*1000)))
		res = self.session.get(records_url, headers=self.headers)
		print(res.text)



if __name__ == '__main__':
    username= input('输入账号：')
    password= input('输入服务密码：')
    login = yidongLogin(username, password)
    login.get_login_info()
    login.get_records()