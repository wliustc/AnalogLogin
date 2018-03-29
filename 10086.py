import requests
import time
import rsa
import re
import binascii
import base64
indexUrl = 'http://www.10086.cn/index/bj/index_100_100.html'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Cookie':'CmLocation=100|100; CmProvid=bj; WT_FPC=id=2a523e624bf8c9eca811521791559658:lv=1521791559658:ss=1521791559658; CaptchaCode=tEquWi; rdmdmd5=0C1C8393CE4A382973436708690EF6D3; lgToken=00f7125b961347d09c36e83becc4e88c',
    'Host':'login.10086.cn',
    'Referer':'https://login.10086.cn/login.html?channelID=12034&backUrl=http%3A%2F%2Fwww.10086.cn%2Findex%2Fbj%2Findex_100_100.html'
}
s = requests.Session()


url2 = 'https://login.10086.cn/login.html?channelID=12034&backUrl=http%3A%2F%2Fwww.10086.cn%2Findex%2Fbj%2Findex_100_100.html'
res2 = s.get(url2,headers=headers)

randomUrl = 'https://login.10086.cn/sendRandomCodeAction.action'
randomData = {
    'userName':'15101528779',
    'type':'01',
    'channelID':'12034'
}
randomRes = s.post(randomUrl,data=randomData,headers=headers)
print(randomRes.text)
smsPwd = input('请输入验证码:')
pwd =  'MjWpM101yX0BPUKoK2Wcjx3z7//R0Yil7q+1LDPIQuKU3dn+jH2a7c2uNhP7Vt07bIWP/AC7NjMNVfDUwPcLq53pmsQN3uZtEpaby6HJK1aWEb2r/6wpYQeNM/WJ6RNJSHQUZWBX8I2kRKWGFfIZoI6FLM1gS2/pbzppyI7j/49ZdUBOYohptL27K0MCA8FNDWK95ekaD0S+NMxp7S21ynlRGDLk6LwNucSobz/s8kH3Vg7TxtIcjIBSfWuXeEsUK3aTXjEl4llh+setL9EQiXUuM1SGsGC4V6lrMzaBckHvsjDN3jWyduyK/jlaxSn8zX/M1s4T4thsP'
loginUrl = 'https://login.10086.cn/login.htm'
loginData = {
    'accountType':'01',
    'account':'15101528779',
    'password':pwd,
    'pwdType':'01',
    'smsPwd':smsPwd,
    'inputCode':'',
    'backUrl':'http://www.10086.cn/index/bj/index_100_100.html',
    'rememberMe':'0',
    'channelID':'12034',
    'protocol':'https:',
    'timestamp':str(int(time.time()*1000))
}
try:
    loginRes = s.get(loginUrl, params=loginData, headers=headers)
    print(loginRes.status_code)
except Exception as e:
    print(e)
res = s.get('http://shop.10086.cn/i/?f=home',headers=headers)
print(s.cookies)
print(s.headers)
# with open('asd.html','w',encoding='utf-8') as f:
#     f.write(s.cookies)
# keyurl = 'https://login.10086.cn/platform/js/encrypt.js?resVer=20141125'
# pubText = requests.get(keyurl).text
# res = re.findall('var key = "(.+)";',pubText)[0]
# print(res.encode())
# rsaPublickey = int(res.encode())
# key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
# print(key)
# password = '123456'
# passwd = rsa.encrypt(password.encode(), key) #加密
# passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。


