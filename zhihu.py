# import requests
# from fake_useragent import UserAgent
# import hashlib
# import time
# import hmac
# import re
# s = requests.session()
# headers = {
#     'Connection': 'keep-alive',
#     'Host': 'www.zhihu.com',
#     'Referer': 'https://www.zhihu.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# }
# url1= 'https://www.zhihu.com/signup?next=%2F'
# urlres = s.get(url1,headers=headers)
#
# xudid = re.findall(r'xUDID&quot;:(.+)&quot;\},&quot;accou',urlres.text)[0]
# headers.update({
#             'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
#             'X-Xsrftoken': s.cookies.get('_xsrf'),
#         })
# def _get_signurate(timestamp):
#     hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
#     grant_type = 'password'
#     client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
#     source = 'com.zhihu.web'
#     hm.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
#     print(hm.hexdigest())
#     return hm.hexdigest()
#
#
# def get_time():
#     return str(int(time.time()*1000))
# timestamp = get_time()
# def captcha():
#
#     captchaurl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
#     res = s.get(captchaurl,headers=headers)
#     print(res.text)
# captcha()
#
# post_data = {
#     'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
#     'grant_type':'password',
#     'timestamp':get_time(),
#     'source':'com.zhihu.web',
#     'signature':_get_signurate(get_time()),
#     'username':'+8615101528779',
#     'password':'aq918927',
#     'captcha':'',
#     'lang':'cn',
#     'ref_source':'homepage',
#     'utm_source':'',
# }
# loginUrl = 'https://www.zhihu.com/api/v3/oauth/sign_in'
# print(post_data)
# res = s.post(loginUrl,data=post_data,headers=headers)
# print(res.text)
# print(s.get('https://www.zhihu.com/api/v4/members/wang-ming-ming-30-72/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20',headers=headers).text)
#


# def test(a,b):
#     result = func(a,b)
#     return result
#
# num = test(11,22,lambda x,y: x+y)
# print(num)

s = {'q_c0': '2|1:0|10:1522661295|4:q_c0|80:MS4xMnhKOEFBQUFBQUFtQUFBQVlBSlZUYTlGcjFzSFE2Z1pmajJlWG9wY0hpWUdnOFA5Vm1rVEdBPT0=|6e5ea49a182b64f7925a7d22e431af5e0895963957d19ab57556b97c71189a9c', 'z_c0': '2|1:0|10:1522661295|4:z_c0|80:MS4xMnhKOEFBQUFBQUFtQUFBQVlBSlZUYTlGcjFzSFE2Z1pmajJlWG9wY0hpWUdnOFA5Vm1rVEdBPT0=|2e806e0d05791df59b37ac3c0a0ab2647f359b3e78c28298affa71108dde6366', '_xsrf': None}
print(type(s))
for i,d in enumerate(s):
    print(d)

    {'avatar_url_template': 'https://pic4.zhimg.com/v2-2e3731109a61363db1c7026ccb3a95f8_{size}.jpg',
     'uid': 60780879806464,
     'follow_notifications_count': 0,
     'user_type': 'people',
     'editor_info': [],
     'headline': '',
     'default_notifications_count': 1,
     'url_token': 'wang-ming-ming-30-72',
     'id': '006f4574c6ed1ef3cc6fe7f95b678a74',
     'messages_count': 1,
     'type': 'people',
     'name': '王明明',
     'url': 'http://www.zhihu.com/api/v4/people/006f4574c6ed1ef3cc6fe7f95b678a74',
     'gender': 1,
     'visits_count': 179,
     'is_advertiser': False,
     'avatar_url': 'https://pic4.zhimg.com/v2-2e3731109a61363db1c7026ccb3a95f8_is.jpg',
     'is_org': False,
     'badge': [], 
     'vote_thank_notifications_count': 0}
