import requests
import re
from PIL import Image
s = requests.session()
headers = {
    'user-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Host':'accounts.douban.com'
}
loginUrl = 'https://accounts.douban.com/login'
def get_captcha(loginUrl):
    # 获取验证码图片
    res = s.get(loginUrl, headers=headers)
    imgurl = re.findall('captcha_image" src="(https://.+=s)" alt="captcha"', res.text)[0]
    with open('captcha.png', 'wb') as f:
        f.write(s.get(imgurl).content)
    captcha_id = re.findall('captcha\?id=(.+:en)', imgurl, re.S)[0]
    # 返回图片id
    return captcha_id
def login(loginUrl):
    # 获取id
    captcha_id = get_captcha(loginUrl)
    im = Image.open('captcha.png')
    im.show()
    captcha = input('请输入验证码：')
    im.close()
    post_data = {
        'source': 'None',
        'redir': 'https://www.douban.com',
        'form_email': '15101528779',
        'form_password': '918927an',
        'captcha-solution': captcha,
        'captcha-id': captcha_id,
        'login': '登录'
    }
    res = s.post(loginUrl, data=post_data, headers=headers).text
    if '验证码不正确' in res:
        print('login failed retry!')
        login(loginUrl)
    else:
        print('login success')

login(loginUrl)