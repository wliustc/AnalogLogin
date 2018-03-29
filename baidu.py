import random
import requests
import rsa
import re
import binascii
import base64
import time

session  = requests.Session()
def make_gid(x):
    t = bin(int(16 * random.random()))
    t = int(t, 2) + int(str(bin(0)), 2)
    t = '{:x}'.format(t)
    return t
s = "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"

gid = re.sub('[xy]',make_gid,s).upper()

url = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt={}&class=login&gid={}&loginversion=v4&logintype=dialogLogin&traceid=&callback=bd__cbs__sxw8no'.format(int(time.time()*1000),gid)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
first_url = 'https://www.baidu.com/'
first_req= session.get(first_url,headers=headers)
session.headers=headers

token_res = session.get(url, headers=headers)
token_pat = '"token" : "(.+)",\s+"cookie"'
token = re.findall(token_pat,token_res.text)[0]

code_res  = session.get('https://passport.baidu.com/v2/api/?logincheck&token={}&tpl=mn&apiver=v3&tt=1520994171356&sub_source=leadsetpwd&username=15227230337&loginversion=v4&dv=tk0.433157143458944961520994143092%40sHU0or6mw-Baw-8Hwa8mwl6mwlBTwiBTwXBawX8mw-6GVf6Grl4k0l6mw-6lVf6Gvl4k0iBmw-B1qf6GLw4k0X8Hw-8G2f61qa4krwBQ__sU0Fz8GLf6m-svsynsVpBoibvsihO6GhOoFAlJot82Ei34krK616X4krwBUw-6k0f6m-svsynsVpBoibvsihO6GhOoFAlJot82Ei34krK6l6K4krwBUwy8mww4pDhGVRHvsiOoihGspx-6pbORoB3LVyNIEsf612iBGsf61qKOkVX4kqfA0p8DithGAbOspBvol0woibiLKAaGYpcJHwaB1Lw6Twa6kJx6Gql4kqfA0p8DithGAbOspBvol0woibiLKAaGYpcJHwaB1QXBHwa6kJxkU0Zr6GqF6TwF8kqf6Gv~8ksf4krwBUwiB16fBGv-4kri610-4pDhGVRHvsiOoihGspx-6pbOJYbaIHwa6kJx-rrJzrFORrMPhFUi6Hwa4k2~xUqR5fw41vl6l0iBl0~6lvi8kV~BkVK6Gsa6kVyBk0~6lqy6Q__iUpPnD~Ln6g4abFRFLe2YpSJnse2Kbc4a-iIYD3JY3eJEv_~U0srBl0fBG0f6GraBaw-61qK4kriB1qf6Gv~6mwaBG2w4k0aBk6f6G6aBq__&traceid=&callback=bd__cbs__yc19mg'.format(token),headers=headers)

code = re.findall('''"codeString" : "([0-9a-zA-Z]+)",''',code_res.text)[0]

vifery_url = 'https://passport.baidu.com/cgi-bin/genimage?{}'.format(code)

pubkey_url = 'https://passport.baidu.com/v2/getpublickey?token={}&tpl=mn&apiver=v3&tt={}&gid={}&loginversion=v4&traceid=&callback=bd__cbs__q6m18r'.format(token,int(time.time()*1000), gid)

pubkey_res = session.get(pubkey_url)
pubkey = re.findall('''"pubkey":'(.+)',"key"''',pubkey_res.text)[0]
rsakey = re.findall('''"key":'(.+)',''',pubkey_res.text)[0]
# with open('1.txt','w') as f:
#     f.write(pubkey)


key = rsa.PublicKey.load_pkcs1_openssl_pem(open('1.txt','r').read().encode()) #创建公钥
password = 'aq918927'
passwd = rsa.encrypt(password.encode(), key) #加密
password = base64.encodebytes(passwd)

data = '''staticpage:
charset:UTF-8
token:509f2afbba2e0c716640fc66222ebc37
tpl:mn
subpro:
apiver:v3
tt:1520935834160
codestring:tcG4707e2731b3ac10c022915729801137b257044063d05312b
safeflg:0
u:https://www.baidu.com/
isPhone:
detect:1
gid:EBB7A6E-4C16-41D2-BACE-B0BEE08C8FDE
quick_user:0
logintype:dialogLogin
logLoginType:pc_loginDialog
idc:
loginmerge:true
splogin:rate
username:1231231
password:p6R9P1i+AJ8b2IhyBXEibOCZBQtO7HeImNy1MDLj8XHW2Y4ZGn6uGUN7HE8YnGDAHX1reQ88MevHgimkm5dXVHQ51SWUQM6AqyJVq2n1N784LarZP1vU7pbX5AOFoyyOYITyvJoR1gv3Cx5PeIxu1uY3vR2CiDk9bLnFVJVt7/A=
verifycode:注重细微
mem_pass:on
rsakey:jtiIYT1ZToT8qNBuN3bVVdXCOgBfskRO
crypttype:12
ppui_logintime:5972564
countrycode:
fp_uid:f6cfa628e11daa90b55dc0948322998c
fp_info:f6cfa628e11daa90b55dc0948322998c002~~~wyww4ClvFkeT48b_kww7tlE4~2k4u3IC0YGllE4~2k4u3IC0cGWwn3scwn3sLwwsawnI0Pl0fwMoGgCuzGv~YG482GC~MzvBrdMoI8vP48vBcWC8cz4BXzKP-8CB7tvBc840PzKeMxC~YWCBXWvBedMkGgpR1JMk2_xkwcMkwc-kwcRkws~l0Wn2oyxSo1lQoFXQkCVQEFTSXpLMRVjSZI1QR1lQoF8FkePpqpAQRFJ6ECeQUCeMkpLMUsJ7qel7EC5QkpbFXV47qFP6EhLSRePpEy~QkztpEztaljkpqn86EyTv~XTCZ-za~XGC8cAul0YtpoFR7qFJSuz~QkViSEzA7k1t6EyTMW-zpR2Gvonl7~XVCB7xC03tpBbIpE1~4~MtC~4I484zCR2kpE7I4RCRC0r~poYz78nj7k7G4B7Vv0s~4kbI4R4-KRrepR1VQurd7kyiQqFT6ECjSoeLQUCd4k7k48M87RpevonjvBYtpB7WCR4-4Bnj487VCBrl78eRpRXGp~XGpB2-pRbWCo7x4~rR7EXI484W7kFR48pepUzep0C~784x4EYkC~MzC~Yx7~rRp0FP4E4VCBsj4BMtCEYxvBSPpRYkv0njv0sjCRCl7~eRvECR40PkC~bGCkbkK~Mz7R4zpBMzCo7-pobICBcz401l7R7tv07-4RXW40j~4R7k78XtCR4zv0nl4EbV4knevBClCk2W7kYz403kCB7_DkwsOkwsrkwsEkwsGwwbAlvOR3iYt-_vlESEz5QRyWQ3__wkwsswwcfkwcNkwchkwcbkwcekwcSlWaBXTC0bIC0Y-v0b8v0MtC8btCY__
loginversion:v4
dv:tk0.102539011305933461520929861648@hhf0RC8kOdBmts9szrsO286Xx9sXhTB0hT6fCYG6vAEFX34kBf8kOY80JdB1qwTksw4kqdCn2ADXvh0CxTs2896Ynw6XxXu~Cy0U2cGHwY8Y9z8kBy4kpwBrwXBHww42Dh0OKH9sXT6Xh0s2etB2xTK683uOzSPFsdBYubA09zBWwyBkhe8kOdBmts9szrsO286Xx9sXhTB0hT6fCYG6vAEFX34kBf8kO~B1OdB1qwTksw4kqdCn2ADXvh0CxTs2896Ynw6XxXu~Cy0U2cGHwY8Y9z8Ynb4kpwBrw_of0whB0pY8yw~A0Bd8ksy8kqd4kpwBrw-8WwYBkBdB1qYAkJX4mwyBkhe8Ysb4kpXBmwyBkOyBksd4kpwBrwf8kEdB0Oy4kptBYBy8WwdB1qwTknt8Ysd8Yq-4kpyBYOf8mwdB1qwTq__x~~GC~y2t-MNhyfiBHwy4kEbBfsKodw41nwB1sYA0qtB0Bw80OYBY9~B0syBkOyA0J~B0EbAq__ifnNrDburBi4yxfKfujEU2MGrsjE~xc4ytXPUD3GU3jGF9_uf0h~BY9b4kBY8WwtB1Jt4kOf8mwy80Ew4knb8kqdB1s~BmwtB1Of4knwA0p_Ff0e~Bmwz4kny4kpw4kp~4kp-4kpz4kBX4k9b4k9X4ksw4ksf4kOb4knw8ywtB0udB0sY4knfBywt8YEdB0J~4knzAHwyBkq_
traceid:031AB801
callback:parent.bd__pcbs__v1g35p'''.split('\n')

post_data = {}
for i in data:
    i=i.split(':')
    post_data[i[0]]=i[1]

post_data['staticpage']='https://www.baidu.com/cache/user/html/v3Jump.html'
post_data['token'] = token
post_data['tt'] = str(int(time.time()*1000))
post_data['gid'] = gid
post_data['password'] = password
post_data['rsakey'] = rsakey
post_data['username'] = '15227230337'
post_data['traceid']='EFBDA901'
post_url = 'https://passport.baidu.com/v2/api/?login'
post_res = session.post(post_url,data=post_data,headers=headers)
asdad = session.get('http://tieba.baidu.com/tbmall/mymall',headers=headers)
print(post_res.headers)
