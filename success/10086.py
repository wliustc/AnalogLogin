import requests
import time
import random
import urllib.parse
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from PIL import Image
username = '15101528779'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Host':'login.10086.cn',
    'Referer':'https://login.10086.cn/html/window/loginMini.html?channelID=12003&backUrl=http://shop.10086.cn/i/sso.html'
}
# def get_wt_fpc():
#     # '''id=20676f6a7dfdb6cb7c81522416169921:
#     # lv=1522416169921:
#     # ss=1522416169921'''
#     t = '2'
#     x = str(int(time.time()*1000))
#     for i in range(2,32-len(x)+1):
#         t+='{:x}'.format(int(random.random()*16.0))
#         t+=x
#     t = urllib.parse.quote_plus(t)
#     print(t)
#     return t
# def get_clooect_id():
# 	collect_id = ''
# 	while len(collect_id) < 32:
# 		ls = '123456798abcdefghijklmnopqrstuvwxyz'
# 		collect_id += random.choice(list(ls))
# 	print(collect_id)
# 	return collect_id
s = requests.session()
def get_login_captcha():
    s.get('http://shop.10086.cn/i/v1/auth/loginfo?_='+str(int(time.time()*1000)),headers=headers)
    indexUrl = 'http://shop.10086.cn/i/?f=home'
    res2 = s.get(indexUrl,headers=headers)
    randomUrl = 'https://login.10086.cn/sendRandomCodeAction.action'
    randomData = {
        'userName':username,
        'type':'01',
        'channelID':'12034'
    }
    randomRes = s.post(randomUrl,data=randomData,headers=headers)
    if randomRes.text == '0':
        print('登录验证码发送成功')
    else:
        print('发送失败')
cookies = {
        'CmLocation': '100|100',
        'CmProvid': 'bj',
        'ssologinprovince': '100'
    }
def get_pubkey():
    url = 'https://login.10086.cn/platform/js/encrypt.js?resVer=20141125'
    print(s.get(url).text)

pubkey = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsgDq4OqxuEisnk2F0EJF
mw4xKa5IrcqEYHvqxPs2CHEg2kolhfWA2SjNuGAHxyDDE5MLtOvzuXjBx/5YJtc9
zj2xR/0moesS+Vi/xtG1tkVaTCba+TV+Y5C61iyr3FGqr+KOD4/XECu0Xky1W9Zm
maFADmZi7+6gO9wjgVpU9aLcBcw/loHOeJrCqjp7pA98hRJRY+MML8MK15mnC4eb
ooOva+mJlstW6t/1lghR8WNV8cocxgcHHuXBxgns2MlACQbSdJ8c6Z3RQeRZBzyj
fey6JCCfbEKouVrWIUuPphBL3OANfgp0B+QG31bapvePTfXU48TYK0M5kE+8Lgbb
WQIDAQAB
-----END PUBLIC KEY-----'''
def get_pwd(pwd):


    rsakey = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsakey)
    text = base64.b64encode(cipher.encrypt(pwd.encode()))
    return text.decode()

def get_login_info():
    get_login_captcha()
    smsPwd = input('请输入验证码:')

    loginUrl = 'https://login.10086.cn/login.htm'
    loginData = {
        'accountType': '01',
        'account': username,
        'password': get_pwd('960128'),
        'pwdType': '01',
        'smsPwd': smsPwd,
        'inputCode': '',
        'backUrl': 'http://shop.10086.cn/i/sso.html',
        'rememberMe': '0',
        'channelID': '12034',
        'protocol': 'https:',
    }


    loginRes = s.get(loginUrl, params=loginData, headers=headers)
    print('denglu jieguo %s ' % loginRes)
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
    s.get(artifactUrl, headers=headers, cookies=cookies)

    infourl = 'http://shop.10086.cn/i/v1/cust/info/' + username + '?_=' + str(int(time.time() * 1000))
    infores = s.get(infourl, headers=headers, cookies=cookies)
    print('gerenxinxi %s ' % infores.text)
    # for i in s.cookies:
    #     print('info %s' % i)
    # # 详单验证码url
    # detailCaptchaUrl = 'http://shop.10086.cn/i/authImg?t='+str(int(time.time()*1000))
    # detailCaptchares = s.get(detailCaptchaUrl,headers=headers,cookies=cookies)
    # with open('detialcaptcha.png','wb') as f:
    #     f.write(detailCaptchares.content)
    # im = Image.open('detialcaptcha.png')
    # im.show()
    # captchaCode = input('验证码:')
    # im.close()
    # captcha_return ='http://shop.10086.cn/i/v1/res/precheck/'+username+'?captchaVal={}&_={}'.format(captchaCode,str(int(time.time()*1000)))
    # captcha_res = s.get(captcha_return, headers=headers, cookies=cookies).text

    print(captcha_res)
    # cookies = {
    #     'CmLocation': '100|100',
    #     'CmProvid': 'bj',
    #     'ssologinprovince': '100',
    #     'CaptchaCode':captchaCode
    # }
    # detailRandomUrl = 'https://shop.10086.cn/i/v1/fee/detbillrandomcodejsonp/'+username+'?callback=jQuery183012222690509809175_1522550487611&_='+str(int(time.time()*1000))
    # detailRandomRes = s.get(detailRandomUrl,headers=headers,cookies=cookies).text
    # print('随机码 %s' % detailRandomRes)
	#
    # randomCode = input('短信随机码:')
    # def pwdcode(s):
    #     print(base64.b64encode(s.encode()))
    #     return base64.b64encode(s.encode())
    # detailUrl = 'https://shop.10086.cn/i/v1/fee/detailbilltempidentjsonp/'+username+'?callback=jQuery183012222690509809175_1522550487611&pwdTempSerCode={}&pwdTempRandCode={}&captchaVal={}&_={}'
	#
	#
    # detailUrl= detailUrl.format(get_pwd('960128'),get_pwd(randomCode),captchaCode,str(int(time.time()*1000)))
    # print('通话详情 %s ' % s.get(detailUrl,headers=headers,cookies=cookies).text)
    # for i in s.cookies:
    #     print('detail %s' % i)
#

if __name__ == '__main__':
    get_login_info()
