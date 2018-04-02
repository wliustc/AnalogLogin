import requests
from fake_useragent import UserAgent

s = requests.session()
headers = {
    'user-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    'referer':'https://www.zhihu.com/signup?next=%2F'
}
url1= 'https://www.zhihu.com/signup?next=%2F'
urlres = s.get(url1,headers=headers)
for i in s.cookies:
    print(i)
post_data = {
    'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type':'password',
    'timestamp':'1522397197945',
    'source':'com.zhihu.web',
    'signature':'006d9579a2b258c2c6221eb537d6fe076c748ef8',
    'username':'+8615101528779',
    'password':'aq918927',
    'captcha':'',
    'lang':'cn',
    'ref_source':'homepage',
    'utm_source':'',
}
# loginUrl = 'https://www.zhihu.com/api/v3/oauth/sign_in'
# res = s.post(loginUrl,data=post_data,headers=headers)
# print(res.text)
def captcha():
    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'referer': 'https://www.zhihu.com/signup?next=%2F',
        ':authority':'www.zhihu.com',
        ':method': 'GET',
        ':path': '/api/v3/oauth/captcha?lang=en',
        ':scheme': 'https',
        # 'x-udid': 'APCgew6TXQ2PThDqtuJuEurrVFE9qby_3Wg=',
        # 'x-xsrftoken':'a598e63c-b082-4156-9948-14cb4e9f1e23',
        'pragma':'no-cache',
        'cache-control':'no-cache',
        'accept': 'application/json,text/plain,*/*',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language':'zh-CN,zh;q = 0.9'
    }
    captchaurl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    res = s.get(captchaurl)
    print(res.text)
    s.options('https://zhihu-web-analytics.zhihu.com/api/v1/payload-verification')
    for i in s.cookies:
        print(i)
captcha()