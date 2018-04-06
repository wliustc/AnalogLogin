import random
import requests
import rsa
import re
import binascii
import base64
import time
import math
import base64
import urllib.parse
from PIL import Image
import rsa
from Crypto.PublicKey import RSA
from Crypto.Util import asn1
from Crypto.Cipher import PKCS1_v1_5
import base64
import random
class baiduLogin():
	def __init__(self, username, password):
		'''
		初始化 用户名 密码 session headers
		构造 gid callback参数
		通过gid callback 获取token
		:param username: 用户名
		:param password: 密码
		'''
		self.username = username
		self.password = password
		self.headers = headers = {
    		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
		}
		self.session = requests.session()
		self.gid = self.get_gid()
		self.callback = self.get_callback()
		self.token = self.get_token()


	def get_gid(self,):
		'''
		阅读js文件
		仿造出gid
		:return: gid
		'''

		def make_gid(x):
			t = bin(int(16 * random.random()))
			t = int(t, 2) + int(str(bin(0)), 2)
			t = '{:x}'.format(t)
			return t

		s = "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
		gid = re.sub('[xy]', make_gid, s).upper()
		return gid

	def base(self,num, b):
		return ((num == 0) and '0') or (self.base(num // b, b).lstrip('0') + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

	def get_callback(self):
		'''
		构造callback参数
		:return:  callback
		'''
		data = 'bd__cbs__'
		randomNum = math.floor(2147483648 * random.random())
		return data + self.base(randomNum, 36)

	def get_token(self):
		'''
		通过callba , gid 获取token
		:return: token
		'''

		tokenUrl = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt={}&class=login&gid={}&loginversion=v4&logintype=dialogLogin&traceid=&callback={}'.format(
			int(time.time() * 1000), self.gid, self.callback)
		token_res = self.session.get(tokenUrl, headers=self.headers)
		token_pat = '"token" : "(.+)",\s+"cookie"'
		token = re.findall(token_pat, token_res.text)[0]
		return token

	def createHeadID(self):
		'''
		构造traceid
		:return: traceid
		'''
		t = str(int(time.time() * 1000)) + str(int(90 * random.random() + 10))
		n = hex(int(t))
		i = len(str(n))
		s = str(n)[i - 6:i]

		s = s + '01'
		s = s.upper()
		return s

	def get_rsakey(self):
		'''
		通过已有的token,gid, callback 以及时间戳 获取密钥
		讲pubkey保存到 pub.pem
		:return: rsakey
		'''
		pubkey_url = 'https://passport.baidu.com/v2/getpublickey?token={}&tpl=mn&apiver=v3&tt={}&gid={}&loginversion=v4&traceid=&callback={}'.format(
			self.token, int(time.time() * 1000), self.gid, self.callback)
		pubkey_res = self.session.get(pubkey_url)
		pubkey = re.findall('''"pubkey":'(.+)',"key"''', pubkey_res.text)[0]
		rsakey = re.findall('''"key":'(.+)',''', pubkey_res.text)[0]

		with open('pub.pem', 'w+') as f:
			s = pubkey.split(r'\n')
			for i in s:
				f.write(i)
				f.write('\n')

		return  rsakey

	def get_pwd(self):
		'''
		读取pub.pem中的公钥
		使用RSA加密密码
		:return: 加密后的密码
		'''
		with open('pub.pem', 'r') as f:
			pubkey = f.read()
			rsakey = RSA.importKey(pubkey)
			cipher = PKCS1_v1_5.new(rsakey)
			text = base64.b64encode(cipher.encrypt(self.password.encode()))
			return text.decode()

	def get_captchaCode(self):
		'''
		首先获取验证码类型: vcodetype 和字符: codeString
		通过token, username, callback 获取后
		通过genimage+ codeString 将验证码保存到本地 打开后识别
		手动输入验证码
		:return: codeString , captchaCode
		'''
		dv = 'tk0.40904722587657581522648037169@ppo0k-9DpYrm~nCnj5n32uMeUCnehOrDhOM-Iz8Mt9FBeXAkpjuDpYrR6~Ok0yrGyyA2EhD3HGCneOMehDn2V~r2UOHMuXp3jP7BnY9kqxrGyf9k2V9D6Yrm~nCnj5n32uMeUCnehOrDhOM-Iz8Mt9FBeXAk6zrDnYrR6~Ok3xAkqYI029EethDIUOn2uCMz0yMeUepdIfDZ2L8GyxuDFjAk4xrMyxAkqYI029EethDIUOn2uCMz0yMeUepdIfDZ2L8GyjrDpzAk4xrMy_nofuD4eAkpxufydrD4yA5hPp-rLpvPg8BjbKmeY7dHb71yf9k2V-ss8CsuXspyJhuohrGyfAkFeForHvYyARCy9Dqwuz4fuD6-uRn-uD6~uD4fuRCxrkr-rDFjhorJ5Ewp5raAfU-H-pQFZ2b85nQFdULAf~e7ZEX8ZXQ8BC_~o0psuRnYrz6YrD4yrmy~rD3-Ak4euRqYrDCwrmyfuDFyAk0frDFYrDr~uC__yo0dsrmy~ufyfu1yfufywrGyeu1ye9GyduGy-9myxufyjrmyjuGy~rkCYrDqeAk0fumy~rRnYrD4dAk0-ufyfrDrYrRreAk4xrC__'
		vcodetypeUrl = 'https://passport.baidu.com/v2/api/?logincheck&token={}&tpl=mn&apiver=v3&tt={}&sub_source=leadsetpwd&username={}&loginversion=v4&dv={}+&callback={}'
		vcodetypeUrl = vcodetypeUrl.format(self.token,str(int(time.time())),self.username,dv, self.callback)
		print(vcodetypeUrl)
		vcodetypeRes = self.session.get(vcodetypeUrl).text
		vcodetype  = re.findall('"vcodetype" : "(.+)",        "userid"',vcodetypeRes)[0]
		code_string  = re.findall('"codeString" : "(.+)",\s+"vco',vcodetypeRes)[0]
		# url = 'https://passport.baidu.com/v2/?reggetcodestr&token={}&tpl=mn&apiver=v3&tt={}&fr=login&loginversion=v4&vcodetype={}&traceid=&callback={}'.format(
		# 	token, str(int(time.time() * 1000)), vcodetype, callback)
		# res = session.get(url)
		# verifyStr = re.findall(' "verifyStr" : "(.+)",\s+"verifySign"', res.text)[0]
		# code_string = self.get_captcha_str()
		url = 'https://passport.baidu.com/cgi-bin/genimage?'+code_string
		with open('capthca.png','wb') as f:
			f.write(self.session.get(url).content)
		im  = Image.open('capthca.png')
		im.show()
		captchCode = input('输入验证马:')
		im.close()
		return captchCode,code_string

	def get_login_info(self):
		'''
		登录
		通过get_captchaCode(),get_rsakey() 拿到captchaCode, code_string,rsakey
		构造post_data 伪造post请求
		当返回值含有err_no=0的时候登录成功
		成功后访问个人中心获取用户名打印出来
		:return:
		'''
		captchaCode, code_string =self.get_captchaCode()
		rsakey = self.get_rsakey()
		post_data = {
			'staticpage': 'https://www.baidu.com/cache/user/html/v3Jump.html',
			'charset': 'UTF-8',
			'token': self.token,
			'tpl': 'mn',
			'subpro': '',
			'apiver': 'v3',
			'tt': str(int(time.time() * 1000)),
			'codestring': code_string,
			'safeflg': 0,
			'u': 'https://www.baidu.com/',
			'isPhone': '',
			'detect': 1,
			'gid': self.gid,
			'quick_user': 0,
			'logintype': 'dialogLogin',
			'logLoginType': 'pc_loginDialog',
			'idc': "",
			'loginmerge': 'true',
			'splogin': 'rate',
			'username': self.username,
			'password': self.get_pwd(),
			'verifycode': captchaCode,
			'mem_pass': 'on',
			'rsakey': rsakey,
			'crypttype': 12,
			'ppui_logintime': 16456,
			'countrycode': '',
			'fp_uid': 'cdd72a954107675582d920e6555a8fc0',
			'fp_info': 'cdd72a954107675582d920e6555a8fc0002~~~guggsRs-AjidsTq_zggF~sts-HjsrUYBtu~ssts-HjsrUYBtZ~QgqUaVgqUaGggaFgqWtKs0hgGv~pBrg~7-u~sTH~B-Gg764DGvYT7fsT76ZIBTZgs6ogLfyTB6FK76ZTstfgLiGeB-uIB6oI76iDGj~pOzXNGjH_xzgZLzgZMzgZCzgaEs0QqHvJecvXR5vAo5jBw5bAdcoOkGzwxc1YX5zXR5vATAjifOCO95zANPbBi5QBiGjOkGQaNFCiRFbBW5jOqAowsFCAfPbSkczifObJ-5jgKObgK3RxjOCnTPbJd7-odB1yg3-o~BTZ9Ds0wxOvAzFCANcrg-5jwhcbg9FjXKPbJdGIgisbHg76H~F6B-F6uKBvBzFTq~BtuwBbOiBbOzstOxBtXfB6ixF6HYObHj76qwsvuKsvoeBzqgF-iiBbBis6ZTLzoeBzHeF-a-ObHwOzowFjq~ObHYs-x-B6GjBzoe76oTO6sjBTBRBjOxF6fY76HKF-4xBTUTFjq~76nfBvogBv4DOvAzFCANcrg-5jwhcbg9FjXKPbJdGIywO-ojFjFe76xf7bFKB-A-F-HKstfTB-afFb4-7vs~Obuw76qTOvqTsTuyOvOiO6swszswF6oeB6oeF-UTBbHyLzHeB-XxOvoYFzoYF6BzOvqTO-HTsjA-F-ujBTqy7vFYObOx76BRB-nzs-xiFzX-B-UK76FIBTnxO-syF6iRsvXDO-cfB-ojB6fj7vFgs-XxsvHYBTFK7bq~BtHgs6fgB6ueBvq~B-ZyFj4iF-oTObXxOzsIF6UeFbHjB-ZIBtafsU__OzgavzgayzgatzgaZggqHs-0zUhuKy_-stcbgW5zJI5U__gzgaBggZhzgZUzgZbzgZTzgZazgZksQ36odBtqYBtuy7tqT7tGKBTqKBu__',
			'loginversion': 'v4',
			'dv': 'tk0.7968740730185651522641031232@vCj0irpmwj8kt~8k4f8kpl8kpf8kpV8kIy8kIX8kOy8kOi8ktwpmwypktUpEqf8ktyAGwyp-PUpE9-8ktVpGw~pkPUp34j8k4~nq__vj0vunEPUpmyIrIiuIBvAHjZrIjhTpEhTHfo-JH0n9Lj58k4ypk4Up34VTktwpGww8v6hEBMGrIjTHjhEIvbypvZTMHA5PBi1CLIUp34~pmw~p31bnEOUpmyIrIiuIBvAHjZrIjhTpEhTHfo-JH0n9Lj58k4lpEBUp34VTkBV8kqUotvn6j0hEoZTIvArH-twHjZjPXo~ENvgJGw~AEIV8k4~nuwypkpUpmyIrIiuIBvAHjZrIjhTpEhTHfo-JH0n9Lj58k4VpkIUp34VTq__lj0BvA3py8k9wpGwXp3pX8v6hEBMGrIjTHjhEIvbypvZTMNo~DLJirXZBJI5gJ~w~p31bAEqi8k9wnGwfA3q~8v6hEBMGrIjTHjhEIvbypvZTMNo~DLJirXZBJGw~p31b~rrJurIuQDwDhIjgpGw~8k9jwjeMsUw83PiA3OfAkqfp-qynkIXAEtjp34XAktwp-t~p-4_gjeDu6lPupK8~ZfMfPS9NvWJuIS9XZg8~yjCN65JN5SJLr_-j0vrA3IUp-OUpE4wpmwypEBf8k4jA3qUpErlpmw~AE9w8kt~pE9UpEpyAr__',
			'traceid': 'D9284401',
			'callback': 'parent.' + self.callback
		}
		post_url = 'https://passport.baidu.com/v2/api/?login'
		post_res = self.session.post(post_url, data=post_data, headers=self.headers)
		#当返回值有err_no=0时登录成功
		result= re.findall('err_no=(\d+)',post_res.text)[0]
		print(result)
		if result == '0':

			home_page = self.session.get('http://i.baidu.com/', headers=self.headers).text
			user = re.findall('class="ibx-uc-nick">(.+)</a>',home_page)[0]
			print('登录成功 %s ' % user)
		elif result == '6':
			print('验证码错误')
			self.get_login_info()
		elif result == '7':
			print('密码错误')
			self.get_login_info()
if __name__ == '__main__':
    username = input('输入用户名：')
    password = input('输入密码：')
    logind = baiduLogin(username,password)
    logind.get_login_info()